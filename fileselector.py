import os
import curses
import xml.etree.ElementTree as ET

class Node:
    def __init__(self, path, parent=None, exclude_files=None, exclude_extensions=None):
        self.path = os.path.normpath(path).replace("\\", "/")
        self.parent = parent
        self.expanded = False
        self.children = []
        self.selected = False
        self.is_dir = os.path.isdir(path)
        self.exclude_files = exclude_files or []
        self.exclude_extensions = exclude_extensions or []
        self.short_description = ""
        self.full_description = ""

    def toggle_expanded(self):
        if self.is_dir:
            self.expanded = not self.expanded

    def ensure_children_loaded(self):
        if self.is_dir and not self.children:
            self._load_children()

    def _load_children(self):
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
        self.ensure_children_loaded()
        files = []
        for child in self.children:
            files.extend(child.get_all_files())
        return files

    def toggle_selected(self):
        self.selected = not self.selected
        if self.is_dir:
            self.ensure_children_loaded()
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
    def __init__(self, root_path, exclude_files=None, exclude_extensions=None, selected_files=None):
        self.exclude_files = exclude_files or []
        self.exclude_extensions = [ext.lower() for ext in (exclude_extensions or [])]
        self.root = Node(root_path, exclude_files=self.exclude_files, exclude_extensions=self.exclude_extensions)
        self.root.expanded = True
        self.root.ensure_children_loaded()
        self.cursor = 0
        self.offset = 0
        self.file_descriptions = self.load_file_descriptions(".system/application_plan.xml")
        self.screen_height = 0
        self.screen_width = 0
        self.selected_files = [os.path.normpath(f).replace("\\", "/") for f in (selected_files or [])]
        self._expand_selected_paths()
        self._initial_select(self.root)

    def _expand_selected_paths(self):
        for selected_file in self.selected_files:
            parts = selected_file.split("/")
            if parts[0] == ".":
                parts = parts[1:]
            self._expand_path(self.root, parts)

    def _expand_path(self, node, path_parts):
        if not path_parts:
            return
        
        node.ensure_children_loaded()
        for child in node.children:
            if os.path.basename(child.path) == path_parts[0]:
                if child.is_dir:
                    child.expanded = True
                    self._expand_path(child, path_parts[1:])
                break


    def _initial_select(self, node):
        rel_path = os.path.relpath(node.path, self.root.path).replace("\\", "/")
        for selected_file in self.selected_files:
            if selected_file.startswith("./"):
                selected_file = selected_file[2:]
            if rel_path == selected_file:
                node.selected = True
                break
        if node.is_dir and node.expanded:
            node.ensure_children_loaded()
            for child in node.children:
                self._initial_select(child)
                
    def load_file_descriptions(self, xml_file):
        descriptions = {}
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for file_elem in root.findall(".//file"):
                name = file_elem.find("name").text
                description = file_elem.find("description").text.strip()
                short_desc = description.split('\n')[0].strip()
                descriptions[name] = (short_desc, description)
        except Exception as e:
            print(f"Error parsing XML: {e} Current working directory: {os.getcwd()}")
        return descriptions

    def run(self):
        return curses.wrapper(self._run) 


    def _run(self, stdscr):
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        
        # Enable keypad input and disable input echoing
        stdscr.keypad(1)
        curses.noecho()

        # Enable color if supported
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

        # Initial screen setup
        self._handle_resize(stdscr)
        
        while True:
            self._draw(stdscr)
            key = stdscr.getch()
            
            if key == ord('q'):
                break
            elif key == curses.KEY_RESIZE:
                self._handle_resize(stdscr)
            elif key == curses.KEY_UP:
                self.cursor = max(0, self.cursor - 1)
            elif key == curses.KEY_DOWN:
                self.cursor = min(len(self._get_visible_nodes()) - 1, self.cursor + 1)
            elif key == ord('\n'):  # Enter key
                node = self._get_visible_nodes()[self.cursor]
                if node.is_dir:
                    node.toggle_expanded()
            elif key == ord(' '):  # Space key
                node = self._get_visible_nodes()[self.cursor]
                node.toggle_selected()
            elif key == ord('h'):  # Help key
                self._show_help(stdscr)
            elif key == ord('i'):  # Info key
                self._show_full_description(stdscr)
            
            self._adjust_offset(stdscr)

        return self._get_selected_files()

    def _handle_resize(self, stdscr):
        self.screen_height, self.screen_width = stdscr.getmaxyx()
        self._adjust_offset(stdscr)
        stdscr.clear()
        curses.resize_term(self.screen_height, self.screen_width)
        stdscr.refresh()

    def _draw(self, stdscr):
        stdscr.clear()
        visible_nodes = self._get_visible_nodes()
        for i, node in enumerate(visible_nodes[self.offset:self.offset+self.screen_height-2]):
            if i + self.offset == self.cursor:
                stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
            
            depth = node.path.count(os.sep) - self.root.path.count(os.sep)
            prefix = "  " * depth
            prefix += "[-] " if node.is_dir and node.expanded else "[+] " if node.is_dir else "    "
            prefix += "[*] " if node.selected else "[ ] "
            
            # Use os.path.relpath to get the relative path from the root
            rel_path = os.path.relpath(node.path, self.root.path).replace("\\", "/")
            if rel_path == ".":
                rel_path = os.path.basename(self.root.path)
            
            line = f"{prefix}{rel_path}"
            
            # Add short description if available
            if rel_path in self.file_descriptions:
                short_desc = self.file_descriptions[rel_path][0]
                available_width = self.screen_width - len(line) - 3
                if available_width > 0:
                    line += f" - {short_desc[:available_width]}"
            
            if len(line) > self.screen_width - 1:
                line = line[:self.screen_width - 4] + "..."
            stdscr.addnstr(i, 0, line, self.screen_width - 1)
            
            if i + self.offset == self.cursor:
                stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        
        # Draw menu
        menu = "↑↓:Move  Enter:Expand  Space:Select  i:Info  h:Help  q:Quit"
        stdscr.addnstr(self.screen_height-1, 0, menu, self.screen_width - 1)
        stdscr.refresh()

    def _adjust_offset(self, stdscr):
        if self.cursor < self.offset:
            self.offset = self.cursor
        elif self.cursor >= self.offset + self.screen_height - 2:
            self.offset = self.cursor - self.screen_height + 3


    def _get_all_nodes(self):
        def traverse(node):
            yield node
            if node.is_dir and node.expanded:
                node.ensure_children_loaded()
                for child in node.children:
                    yield from traverse(child)
        
        return list(traverse(self.root))

    def _get_visible_nodes(self):
        return [node for node in self._get_all_nodes() if self._is_visible(node)]

    def _is_visible(self, node):
        if node == self.root:
            return True
        parent = node.parent
        while parent:
            if not parent.expanded:
                return False
            parent = parent.parent
        return True
    
    def _get_selected_files(self):
        selected_files = []
        for node in self._get_all_nodes():
            if node.selected:
                selected_files.extend(node.get_all_files())
        return list(set(selected_files))  # Remove duplicates

    def _show_help(self, stdscr):
        help_text = [
            "File Tree Selector Help",
            "",
            "↑/↓: Move cursor up/down",
            "Enter: Toggle expand folder",
            "Space: Toggle select file or folder",
            "i: Show full description of the file",
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
        self._show_text_box(stdscr, "Help", '\n'.join(help_text))

    def _show_full_description(self, stdscr):
        node = self._get_visible_nodes()[self.cursor]
        # filename = os.path.basename(node.path)
        filename = node.path.replace("\\", "/")[2:len(node.path.replace("\\", "/"))]
        if filename in self.file_descriptions:
            _, full_desc = self.file_descriptions[filename]
            self._show_text_box(stdscr, f"Description for {filename}", full_desc)

    def _show_text_box(self, stdscr, title, text):
        height, width = stdscr.getmaxyx()
        lines = text.split('\n')
        pad = curses.newpad(len(lines) + 4, max(len(line) for line in lines) + 4)
        pad.addstr(1, 2, title)
        pad.addstr(2, 2, "=" * len(title))
        for i, line in enumerate(lines):
            pad.addstr(i + 3, 2, line)
        pad.box()
        
        pad_height = min(len(lines) + 5, height - 2)
        pad_width = min(max(len(line) for line in lines) + 4, width - 2)
        
        scroll_pos = 0
        while True:
            pad.refresh(scroll_pos, 0, (height - pad_height) // 2, (width - pad_width) // 2, 
                        (height + pad_height) // 2, (width + pad_width) // 2)
            key = stdscr.getch()
            if key in (ord('q'), ord('i'), curses.KEY_ENTER, 10, 13):
                break
            elif key == curses.KEY_UP and scroll_pos > 0:
                scroll_pos -= 1
            elif key == curses.KEY_DOWN and scroll_pos < len(lines) - pad_height + 3:
                scroll_pos += 1


def select_files_manually(location=".", our_exclude_files=None, our_exclude_extensions=None, our_selected_files=None):     
    our_exclude_files = our_exclude_files or [".git", ".gitignore", "__pycache__", "venv", ".venv", ".system"]
    our_exclude_extensions = our_exclude_extensions or [".pyc", ".pyo", ".pyd"]
    original_dir = os.getcwd()
    try:
        os.chdir(location)
        selector = FileTreeSelector(".", exclude_files=our_exclude_files, exclude_extensions=our_exclude_extensions, selected_files=our_selected_files)
        selected_files = selector.run()
        # Convert selected_files back to relative paths
        selected_files = [os.path.relpath(file, ".").replace("\\", "/") for file in selected_files]
    finally:
        os.chdir(original_dir)
    return selected_files
        
# Usage example
if __name__ == "__main__":
    original_dir = os.path.join(os.getcwd(),"app")
    exclude_files = [".git", ".gitignore", "__pycache__", "venv", ".venv"]
    exclude_extensions = [".pyc", ".pyo", ".pyd", ".", ".."]
    # selected files are valid relative paths inside the original_dir
    selected_files = ["main.py", "./.venv/pyvenv.cfg",'app/templates/index.html', 'app/static/js/main.js', 'app/routes/messages.py']
    
    selected_files = select_files_manually(
        location=original_dir,
        our_exclude_files=exclude_files,
        our_exclude_extensions=exclude_extensions,
        our_selected_files=selected_files
    )
    
    for file in selected_files:
        print(f"{file}")