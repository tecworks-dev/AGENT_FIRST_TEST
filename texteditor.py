import curses,time,os,sys
from curses.textpad import Textbox, rectangle

def act(stdscr,linestab,fichier):
    tab_fichier = fichier.split(".")
    ext = tab_fichier[-1]
    
    
    for line in linestab:
        if line == "@run":
            linestab.remove(line)
            contentstring = "\n".join(linestab)
            with open(fichier,"w") as f:
                f.write(contentstring)
            if ext == "py":
                os.system(f"xfce4-terminal -e 'python3 {fichier}' --hold")
            elif ext == "js":
                os.system(f"xfce4-terminal -e 'js {fichier}' --hold")
            elif ext == "rb":
                os.system(f"xfce4-terminal -e 'ruby {fichier}' --hold")
            elif ext == "php":
                os.system(f"xfce4-terminal -e 'php {fichier}' --hold")
            
        elif line == "@quit":
            sys.exit()
        elif "@copyto" in line:
            tabline = line.split(" ")
            first = int(tabline[0]) - 1
            last = int(tabline[2]) - 1
            linestab[last] = linestab[first]
            linestab.remove(line)
        elif "@swap" in line:
            tabline = line.split(" ")
            first = int(tabline[0]) - 1
            last = int(tabline[2]) - 1
            linestab[last], linestab[first] = linestab[first],linestab[last]
            linestab.remove(line)
        elif "@remove" in line:
            tabline = line.split(" ")
            first = int(tabline[1]) - 1
            linestab.remove(linestab[first])
            linestab.remove(line)

            
        contentstring = "\n".join(linestab)
        with open(fichier,"w") as f:
            f.write(contentstring)

def main(stdscr):
    cont = True
    while cont:
        h,w = stdscr.getmaxyx()
        wh,ww = stdscr.getmaxyx()
        w -= 1
        h -= 2
        ww -= 2
        wh -= 6
        
        titlewin = curses.newwin(1,ww  - 15,1,16)
        win = curses.newwin(wh,ww,4,1)
        box = Textbox(win)
        titlebox = Textbox(titlewin)
        stdscr.addstr(1,0,"Nom de fichier: ")
        rectangle(stdscr,0,15,2,w)
        rectangle(stdscr,3,0, h, w)
        
        
        stdscr.refresh()
        titlebox.edit()
        box.edit()
        title = titlebox.gather().rstrip()
        text = box.gather().rstrip()
        
        content = text.split("\n")
        titre_fichier = f"/root/Documents/curseseditor/{title}"
        act(stdscr,content,titre_fichier)
        #stdscr.addstr(3,0,contentstring)
        
curses.wrapper(main)