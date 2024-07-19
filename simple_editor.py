import curses
import os

class SimpleEditor:
    def __init__(self, filename):
        self.filename = filename
        self.contents = []
        self.cursor_y = 0
        self.cursor_x = 0
        self.top_line = 0
        self.message = ""

    def load_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.contents = f.read().splitlines()
        if not self.contents:
            self.contents = ['']

    def save_file(self):
        with open(self.filename, 'w') as f:
            f.write('\n'.join(self.contents))
        self.message = f"Saved {self.filename}"

    def run(self):
        return curses.wrapper(self._run)

    def _run(self, stdscr):
        self.load_file()
        curses.curs_set(1)  # Show cursor
        stdscr.clear()

        while True:
            self.display(stdscr)
            ch = stdscr.getch()

            if ch == ord('q'):
                if self.confirm_quit(stdscr):
                    break
            elif ch == curses.KEY_UP:
                self.move_cursor_up()
            elif ch == curses.KEY_DOWN:
                self.move_cursor_down()
            elif ch == curses.KEY_LEFT:
                self.move_cursor_left()
            elif ch == curses.KEY_RIGHT:
                self.move_cursor_right()
            elif ch in (10, 13):  # Enter key
                self.insert_newline()
            elif ch == curses.KEY_BACKSPACE or ch == 127:
                self.backspace()
            elif ch == ord('s'):
                self.save_file()
            elif ch == curses.KEY_RESIZE:
                stdscr.clear()
            else:
                self.insert_char(chr(ch))

    def display(self, stdscr):
        height, width = stdscr.getmaxyx()
        stdscr.clear()

        for i, line in enumerate(self.contents[self.top_line:self.top_line+height-2]):
            if i >= height - 2:
                break
            stdscr.addstr(i, 0, line[:width-1])

        statusbar = f" {self.filename} - Line {self.cursor_y + 1}/{len(self.contents)}"
        stdscr.addstr(height-2, 0, statusbar[:width-1], curses.A_REVERSE)
        
        if self.message:
            stdscr.addstr(height-1, 0, self.message[:width-1])
            self.message = ""

        stdscr.move(self.cursor_y - self.top_line, self.cursor_x)
        stdscr.refresh()

    def move_cursor_up(self):
        if self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = min(self.cursor_x, len(self.contents[self.cursor_y]))
        if self.cursor_y < self.top_line:
            self.top_line = self.cursor_y

    def move_cursor_down(self):
        if self.cursor_y < len(self.contents) - 1:
            self.cursor_y += 1
            self.cursor_x = min(self.cursor_x, len(self.contents[self.cursor_y]))
        if self.cursor_y >= self.top_line + curses.LINES - 2:
            self.top_line = self.cursor_y - curses.LINES + 3

    def move_cursor_left(self):
        if self.cursor_x > 0:
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = len(self.contents[self.cursor_y])

    def move_cursor_right(self):
        if self.cursor_x < len(self.contents[self.cursor_y]):
            self.cursor_x += 1
        elif self.cursor_y < len(self.contents) - 1:
            self.cursor_y += 1
            self.cursor_x = 0

    def insert_newline(self):
        current_line = self.contents[self.cursor_y]
        self.contents[self.cursor_y] = current_line[:self.cursor_x]
        self.contents.insert(self.cursor_y + 1, current_line[self.cursor_x:])
        self.cursor_y += 1
        self.cursor_x = 0

    def backspace(self):
        if self.cursor_x > 0:
            current_line = self.contents[self.cursor_y]
            self.contents[self.cursor_y] = current_line[:self.cursor_x-1] + current_line[self.cursor_x:]
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            current_line = self.contents.pop(self.cursor_y)
            self.cursor_y -= 1
            self.cursor_x = len(self.contents[self.cursor_y])
            self.contents[self.cursor_y] += current_line

    def insert_char(self, char):
        current_line = self.contents[self.cursor_y]
        self.contents[self.cursor_y] = current_line[:self.cursor_x] + char + current_line[self.cursor_x:]
        self.cursor_x += 1

    def confirm_quit(self, stdscr):
        height, width = stdscr.getmaxyx()
        stdscr.addstr(height-1, 0, "Quit without saving? (y/n)", curses.A_REVERSE)
        stdscr.refresh()
        while True:
            ch = stdscr.getch()
            if ch == ord('y'):
                return True
            elif ch == ord('n'):
                stdscr.addstr(height-1, 0, " " * (width-1))
                return False

# Usage example
if __name__ == "__main__":
    editor = SimpleEditor("test.txt")
    editor.run()