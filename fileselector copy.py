import os
import curses

class Node:
    def __init__(self, path, parent=None, exclude_files=None, exclude_extensions=None):
        self.path = path
        self.parent = parent
        self.expanded = False
        self.children = []
        self.selected = False
        self.is_dir = os.path.isdir(path)
        self.exclude_files = exclude_files or []
        self.exclude_extensions = exclude_extensions or []

    def toggle_expanded(self):
        if self.is_dir:
            self.expanded = not self.expanded
            if self.expanded and not self.children:
                self.load_children()

    def load_children(self):
        try:
            for item in sorted(os.listdir(self.path)):
                child_path = os.path.join(self.path, item)
                if not self._is_excluded(child_path):
                    self.children.append(Node(child_path, self, self.exclude_files, self.exclude_extensions))
        except PermissionError:
            pass  # Skip directories we can't access

    def get_all_files(self):
        if not self.is_dir:
            return [self.path]
        files = []
        if not self.children:
            self.load_children()
        for child in self.children:
            files.extend(child.get_all_files())
        return files

    def toggle_selected(self):
        self.selected = not self.selected
        if self.is_dir:
            if not self.children:
                self.load_children()
            self._toggle_children_selected(self.selected)

    def _toggle_children_selected(self, selected):
        for child in self.children:
            child.selected = selected
            if child.is_dir:
                child._toggle_children_selected(selected)

    def _is_excluded(self, path):
        filename = os.path.basename(path)
        _, extension = os.path.splitext(filename)
        return (filename in self.exclude_files or
                extension.lower() in self.exclude_extensions or
                filename.lower() in self.exclude_files)

class FileTreeSelector:
    def __init__(self, root_path, exclude_files=None, exclude_extensions=None):
        self.exclude_files = exclude_files or []
        self.exclude_extensions = [ext.lower() for ext in (exclude_extensions or [])]
        self.root = Node(root_path, exclude_files=self.exclude_files, exclude_extensions=self.exclude_extensions)
        self.root.expanded = True
        self.root.load_children()
        self.cursor = 0
        self.offset = 0

    def run(self):
        return curses.wrapper(self._run)

    def _run(self, stdscr):
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        
        while True:
            self._draw(stdscr)
            key = stdscr.getch()
            
            if key == ord('q'):
                break
            elif key == curses.KEY_UP:
                self.cursor = max(0, self.cursor - 1)
            elif key == curses.KEY_DOWN:
                self.cursor = min(len(self._get_visible_nodes()) - 1, self.cursor + 1)
            elif key == ord('\n'):  # Enter key
                node = self._get_visible_nodes()[self.cursor]
                if node.is_dir:
                    node.toggle_expanded()
                node.toggle_selected()
            elif key == ord(' '):  # Space key
                node = self._get_visible_nodes()[self.cursor]
                node.toggle_selected()
            elif key == ord('h'):  # Help key
                self._show_help(stdscr)
            
            # Adjust offset to keep cursor in view
            height, _ = stdscr.getmaxyx()
            if self.cursor < self.offset:
                self.offset = self.cursor
            elif self.cursor >= self.offset + height - 1:
                self.offset = self.cursor - height + 2

        return self._get_selected_files()

    def _draw(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        visible_nodes = self._get_visible_nodes()
        for i, node in enumerate(visible_nodes[self.offset:self.offset+height-2]):
            if i + self.offset == self.cursor:
                stdscr.attron(curses.A_REVERSE)
            
            prefix = "  " * (node.path.count(os.sep) - self.root.path.count(os.sep))
            if node.is_dir:
                prefix += "[+] " if node.expanded else "[-] "
            else:
                prefix += "    "
            
            if node.selected:
                prefix += "[*] "
            else:
                prefix += "[ ] "
            
            line = f"{prefix}{os.path.basename(node.path)}"
            if len(line) > width - 1:
                line = line[:width - 4] + "..."
            stdscr.addstr(i, 0, line)
            
            if i + self.offset == self.cursor:
                stdscr.attroff(curses.A_REVERSE)
        
        # Draw menu
        menu = "↑↓:Move  Enter:Toggle Expand/Select  Space:Toggle Select  h:Help  q:Quit"
        stdscr.addstr(height-1, 0, menu[:width-1])
        stdscr.refresh()

    def _get_all_nodes(self):
        def traverse(node):
            yield node
            if node.expanded:
                for child in node.children:
                    yield from traverse(child)
        
        return list(traverse(self.root))

    def _get_visible_nodes(self):
        return [node for node in self._get_all_nodes() if self._is_visible(node)]

    def _is_visible(self, node):
        if node == self.root:
            return True
        return self._is_visible(node.parent) and node.parent.expanded

    def _get_selected_files(self):
        selected_files = []
        for node in self._get_all_nodes():
            if node.selected:
                selected_files.extend(node.get_all_files())
        return list(set(selected_files))  # Remove duplicates

    def _show_help(self, stdscr):
        height, width = stdscr.getmaxyx()
        help_text = [
            "File Tree Selector Help",
            "",
            "↑/↓: Move cursor up/down",
            "Enter: Toggle expand folder / Select file or folder",
            "Space: Toggle select file or folder",
            "h: Show this help screen",
            "q: Quit and return selected files",
            "",
            "When a folder is selected, all its contents are selected,",
            "even if the folder is not expanded in the view.",
            "",
            "Excluded files and extensions are not shown in the selector.",
            "",
            "Press any key to close this help screen"
        ]
        
        pad = curses.newpad(len(help_text) + 2, max(len(line) for line in help_text) + 4)
        for i, line in enumerate(help_text):
            pad.addstr(i + 1, 2, line)
        pad.box()
        
        pad_height = min(len(help_text) + 2, height - 2)
        pad_width = min(max(len(line) for line in help_text) + 4, width - 2)
        pad.refresh(0, 0, (height - pad_height) // 2, (width - pad_width) // 2, 
                    (height + pad_height) // 2, (width + pad_width) // 2)
        
        stdscr.getch()  # Wait for key press

# Usage example
if __name__ == "__main__":
    exclude_files = [".git", ".gitignore", "README.md", "__pycache__", "venv", ".venv"]
    exclude_extensions = [".pyc", ".pyo", ".pyd"]
    selector = FileTreeSelector(".", exclude_files=exclude_files, exclude_extensions=exclude_extensions)
    selected_files = selector.run()
    print("Selected files:")
    for file in selected_files:
        print(file)