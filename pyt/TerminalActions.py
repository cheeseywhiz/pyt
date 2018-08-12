import math
from .TerminalBase import TerminalBase

__all__ = 'TerminalActions',


class TerminalActions(TerminalBase):
    def reset(self):
        return type(self)()

    def reset_string_buffer(self, string_type=None):
        self.string_buffer = []
        self.string_type = string_type
        return self

    def reset_csi_buffer(self):
        self.csi_buffer = []
        return self

    def cursor_up(self, n_lines=None):
        if n_lines is None:
            n_lines = 1

        self.cursor = self.cursor.replace(y=self.cursor.y - n_lines)
        return self

    def cursor_down(self, n_lines=None):
        if n_lines is None:
            n_lines = 1

        self.cursor = self.cursor.replace(y=self.cursor.y + n_lines)
        return self

    def cursor_forward(self, n_cols=None):
        if n_cols is None:
            n_cols = 1

        self.cursor = self.cursor.replace(x=self.cursor.x + n_cols)
        return self

    def cursor_backward(self, n_cols=None):
        if n_cols is None:
            n_cols = 1

        self.cursor = self.cursor.replace(x=self.cursor.x - n_cols)
        return self

    def cursor_character_absolute(self, nth_col=None):
        if nth_col is None:
            nth_col = 1

        self.cursor = self.cursor.replace(x=nth_col - 1)
        return self

    def cursor_next_line(self, n_lines=None):
        return self \
            .carriage_return() \
            .cursor_down(n_lines)

    def cursor_preceding_line(self, n_lines=None):
        return self \
            .carriage_return() \
            .cursor_up(n_lines)

    def cursor_position(self, nth_line=None, nth_col=None):
        if nth_line is None:
            nth_line = 1

        if nth_col is None:
            nth_col = 1

        self.cursor = self.cursor.replace(x=nth_col - 1, y=nth_line - 1)
        return self

    def backspace(self):
        return self.cursor_backward()

    def carriage_return(self):
        return self.cursor_character_absolute()

    def line_feed(self):
        return self.cursor_next_line()

    def add_char(self, code_point):
        self.screen[self.cursor] = code_point
        return self.cursor_forward()

    def erase_character(self, n_chars_plus_one=None):
        if n_chars_plus_one is None:
            n_chars_plus_one = 1

        n_chars = n_chars_plus_one - 1
        deleted_keys = []

        for cursor in self.screen.keys():
            if cursor.y == self.cursor.y \
                    and 0 <= cursor.x - self.cursor.x <= n_chars:
                deleted_keys.append(cursor)

        for key in deleted_keys:
            self.screen.pop(key)

        return self

    def erase_in_line(self, selection=None):
        if selection is None:
            selection = 0

        deleted_keys = []

        if selection == 0:
            start = self.cursor.x
            end = math.inf
        elif selection == 1:
            start = 0
            end = self.cursor.x
        elif selection == 2:
            start = 0
            end = math.inf

        for cursor in self.screen.keys():
            if cursor.y == self.cursor.y and start <= cursor.x <= end:
                deleted_keys.append(cursor)

        for key in deleted_keys:
            self.screen.pop(key)

        return self

    def erase_in_page(self, selection=None):
        if selection is None:
            selection = 0

        deleted_keys = []

        if selection == 0:
            x_min = self.cursor.x
            x_max = math.inf
            y_min = self.cursor.y
            y_max = math.inf
        elif selection == 1:
            x_min = 0
            x_max = self.cursor.x
            y_min = 0
            y_max = self.cursor.y
        elif selection == 2:
            x_min = 0
            x_max = math.inf
            y_min = 0
            y_max = math.inf

        for cursor in self.screen.keys():
            if (cursor.y == self.cursor.y and x_min <= cursor.x <= x_max) \
                    or y_min < cursor.y < y_max:
                deleted_keys.append(cursor)

        for key in deleted_keys:
            self.screen.pop(key)

        return self

    def line_position_absolute(self, nth_line=None):
        if nth_line is None:
            nth_line = 1

        self.cursor = self.cursor.replace(y=nth_line - 1)
        return self

    def line_position_backwards(self, n_lines=None):
        if n_lines is None:
            n_lines = 1

        self.cursor = self.cursor.replace(self.cursor.y + n_lines)
        return self

    def line_position_forwards(self, n_lines=None):
        if n_lines is None:
            n_lines = 1

        self.cursor = self.cursor.replace(self.cursor.y - n_lines)
        return self
