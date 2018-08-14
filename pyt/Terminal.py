from . import actions
from . import config
from . import control_codes
from .TerminalActions import TerminalActions
from .ParsedCSI import ParsedCSI
from .NextCharMode import NextCharMode

__all__ = 'Terminal',


def empty_matrix(rows, columns, obj=None):
    row = [obj] * columns
    return [row[:] for _ in range(rows)]


class Terminal(TerminalActions):
    def handle_C0(self, C0):
        if C0 is control_codes.C0.BS:
            return self.backspace()
        if C0 in (
                control_codes.C0.LF,
                control_codes.C0.VT,
                control_codes.C0.FF,
        ):
            return self.line_feed()
        elif C0 is control_codes.C0.CR:
            return self.carriage_return()
        elif C0 is control_codes.C0.ESC:
            self.next_char_mode = NextCharMode.ESC
            return self
        elif C0 is control_codes.C0.HT:
            return self.character_tabulation()

        print(f'Unhandled C0: {C0 !r}')
        return self

    def handle_C1(self, C1):
        self.next_char_mode = NextCharMode.CHAR

        if C1 is control_codes.C1_7B.CSI:
            self.next_char_mode = NextCharMode.CSI
            return self.reset_csi_buffer()
        elif C1 in (
                control_codes.C1_7B.APC,
                control_codes.C1_7B.DCS,
                control_codes.C1_7B.OSC,
                control_codes.C1_7B.PM,
                control_codes.C1_7B.SOS,
        ):
            self.next_char_mode = NextCharMode.STRING
            return self.reset_string_buffer(C1)
        elif C1 is control_codes.C1_7B.NEL:
            return self.add_newline()
        elif C1 is control_codes.C1_7B.RIS:
            return self.reset()
        elif C1 in (
                control_codes.C1_7B.CS0,
                control_codes.C1_7B.CS1,
                control_codes.C1_7B.CS2,
                control_codes.C1_7B.CS3,
        ):
            self.set_char_set_selection = C1
            self.next_char_mode = NextCharMode.SET_CHAR_SET
            return self

        print(f'Unhandled C1: {C1 !r}')
        return self

    def handle_char(self, code_point):
        C0 = control_codes.C0(code_point)

        if C0 is not None:
            return self.handle_C0(C0)

        return self.add_char(code_point)

    def handle_esc(self, code_point):
        C1 = control_codes.C1_7B(code_point)

        if C1 is not None:
            return self.handle_C1(C1)

        print(f'Unknown esc: %s' % hex(code_point))
        self.next_char_mode = NextCharMode.CHAR
        return self

    def ignore_sgr(self, *args):
        return self

    def get_csi_func(self, csi_type):
        return {
            control_codes.CSI.CUU: self.cursor_up,
            control_codes.CSI.CUD: self.cursor_down,
            control_codes.CSI.CUF: self.cursor_forward,
            control_codes.CSI.CUB: self.cursor_backward,
            control_codes.CSI.CNL: self.cursor_next_line,
            control_codes.CSI.CPL: self.cursor_preceding_line,
            control_codes.CSI.CHA: self.cursor_character_absolute,
            control_codes.CSI.CUP: self.cursor_position,
            control_codes.CSI.ECH: self.erase_character,
            control_codes.CSI.ED: self.erase_in_page,
            control_codes.CSI.EL: self.erase_in_line,
            control_codes.CSI.VPA: self.line_position_absolute,
            control_codes.CSI.VPB: self.line_position_backwards,
            control_codes.CSI.VPR: self.line_position_forwards,
            control_codes.CSI.SGR: self.ignore_sgr,  # TODO
        }.get(csi_type)

    def do_csi(self, csi):
        csi_func = self.get_csi_func(csi.csi_type)

        if csi_func is None:
            print(f'Unhandled csi: {csi}')
            return self

        return csi_func(*csi.args)

    def parse_csi(self):
        self.next_char_mode = NextCharMode.CHAR
        csi_string = ''.join(map(chr, self.csi_buffer[:-1]))
        final_byte = control_codes.CSI(self.csi_buffer[-1])
        csi = ParsedCSI(final_byte, csi_string)
        return self \
            .reset_csi_buffer() \
            .do_csi(csi)

    def handle_csi(self, code_point):
        if code_point in range(0x20, 0x30):
            print('Skipping control sequence with intermediate byte '
                  '(%s)' % hex(code_point))
            self.next_char_mode = NextCharMode.CHAR
            return self.reset_csi_buffer()

        final_byte = control_codes.CSI(code_point)

        if final_byte is not None or code_point in range(0x30, 0x40):
            self.csi_buffer.append(code_point)

            if final_byte is not None:
                return self.parse_csi()

            return self

        print(f'Unknown csi: %s' % hex(code_point))
        return self

    def parse_string_impl(self, string_type, string):
        print(f'Received string ({string_type !r}) {string !r}')
        return self

    def parse_string(self):
        self.next_char_mode = NextCharMode.CHAR
        string_type = self.string_type
        string = ''.join(map(chr, self.string_buffer))
        return self \
            .reset_string_buffer() \
            .parse_string_impl(string_type, string)

    def handle_string_C0(self, C0):
        if C0 is control_codes.C0.BEL:
            return self.parse_string()
        elif C0 is control_codes.C0.ESC:
            self.next_char_mode = NextCharMode.STRING_ESC
            return self

        return self

    def handle_string(self, code_point):
        C0 = control_codes.C0(code_point)

        if C0 is not None:
            return self.handle_string_C0(C0)

        self.string_buffer.append(code_point)
        return self

    def handle_string_esc(self, code_point):
        if control_codes.C1_7B(code_point) is control_codes.C1_7B.ST:
            return self.parse_string()
        else:
            # string interrupted
            self.next_char_mode = NextCharMode.ESC
            return self \
                .reset_string_buffer() \
                .handle_esc()

    def handle_set_char_set(self, code_point):
        print('Ignoring character set setting '
              f'{self.set_char_set_selection !r} = {hex(code_point)}')
        self.next_char_mode = NextCharMode.CHAR
        self.set_char_set_selection = None
        return self

    @property
    def put_char_func(self):
        return {
            NextCharMode.CHAR: self.handle_char,
            NextCharMode.ESC: self.handle_esc,
            NextCharMode.CSI: self.handle_csi,
            NextCharMode.STRING: self.handle_string,
            NextCharMode.STRING_ESC: self.handle_string_esc,
            NextCharMode.SET_CHAR_SET: self.handle_set_char_set,
        }[self.next_char_mode]

    def put_code_point(self, code_point):
        return self.put_char_func(code_point)

    def put_byte_sequence(self, byte_sequence):
        self_chain = self

        for code_point in self.unicode_buffer.add_bytes(*byte_sequence):
            self_chain = self_chain.put_code_point(code_point)

        return self_chain

    def put_byte(self, byte):
        return self.put_byte_sequence([byte])

    def put_string(self, string):
        self_chain = self

        for code_point in map(ord, string):
            self_chain = self_chain.put_code_point(code_point)

        return self_chain

    @property
    def screen_str(self):
        width = config.width
        height = config.height
        height = max(
            (cursor.y for cursor in self.screen.keys()),
            default=height - 1,
        ) + 1
        screen = empty_matrix(height, width, ord(' '))

        for cursor, code_point in self.screen.items():
            if cursor.x >= width or cursor.y >= height:
                continue

            screen[cursor.y][cursor.x] = code_point

        return '\n'.join(''.join(map(chr, row)) for row in screen)

    def reduce(self, action=None):
        if isinstance(action, actions.PutByte):
            return self.copy().put_byte(action.byte)
        if isinstance(action, actions.PutByteSequence):
            return self.copy().put_byte_sequence(action.byte_sequence)
        if isinstance(action, actions.PutCodePoint):
            return self.copy().put_code_point(action.code_point)
        elif isinstance(action, actions.PutString):
            return self.copy().put_string(action.string)

        return self
