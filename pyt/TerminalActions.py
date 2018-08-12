__all__ = 'TerminalActions',

INFINITY = float('inf')


class TerminalActions:
    def cursor_up(self, n_lines=None):
        if n_lines is None:
            n_lines = 1

        x, y = self.cursor
        self.cursor = x, y - n_lines
        return self

    def cursor_down(self, n_lines=None):
        if n_lines is None:
            n_lines = 1

        x, y = self.cursor
        self.cursor = x, y + n_lines
        return self

    def cursor_forward(self, n_cols=None):
        if n_cols is None:
            n_cols = 1

        x, y = self.cursor
        self.cursor = x + n_cols, y
        return self

    def cursor_backward(self, n_cols=None):
        if n_cols is None:
            n_cols = 1

        x, y = self.cursor
        self.cursor = x - n_cols, y
        return self

    def cursor_character_absolute(self, nth_col=None):
        if nth_col is None:
            nth_col = 1

        x, y = self.cursor
        self.cursor = nth_col - 1, y
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

        self.cursor = nth_col - 1, nth_line - 1
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
        current_x, current_y = self.cursor
        deleted_keys = []

        for key in self.screen.keys():
            x, y = key

            if y == current_y and 0 <= x - current_x <= n_chars:
                deleted_keys.append(key)

        for key in deleted_keys:
            self.screen.pop(key)

        return self

    def erase_in_line(self, selection=None):
        if selection is None:
            selection = 0

        current_x, current_y = self.cursor
        deleted_keys = []

        if selection == 0:
            start = current_x
            end = INFINITY
        elif selection == 1:
            start = 0
            end = current_x
        elif selection == 2:
            start = 0
            end = INFINITY

        for key in self.screen.keys():
            x, y = key

            if y == current_y and start <= x <= end:
                deleted_keys.append(key)

        for key in deleted_keys:
            self.screen.pop(key)

        return self

    def erase_in_page(self, selection=None):
        if selection is None:
            selection = 0

        current_x, current_y = self.cursor
        deleted_keys = []

        if selection == 0:
            x_min = current_x
            x_max = INFINITY
            y_min = current_y
            y_max = INFINITY
        elif selection == 1:
            x_min = 0
            x_max = current_x
            y_min = 0
            y_max = current_y
        elif selection == 2:
            x_min = 0
            x_max = INFINITY
            y_min = 0
            y_max = INFINITY

        for key in self.screen.keys():
            x, y = key

            if y_min < y < y_max or (y == current_y and x_min <= x <= x_max):
                deleted_keys.append(key)

        for key in deleted_keys:
            self.screen.pop(key)

        return self

    def reset(self):
        return type(self)()

    def reset_string_buffer(self, string_type=None):
        self.string_buffer = []
        self.string_type = string_type
        return self

    def reset_csi_buffer(self):
        self.csi_buffer = []
        return self
