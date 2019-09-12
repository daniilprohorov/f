import curses
import os
import subprocess as s

def init():
    mmask = curses.ALL_MOUSE_EVENTS
    screen = curses.initscr()
    curses.curs_set(0)
    screen.keypad(1)
    curses.mousemask(mmask)
    curses.noecho()
    return (curses, screen)


def exit(curses):
    curses.endwin()

def folder(name):
    w = 16
    h = 7
    f1 ="  ╔══════════╗        "    
    f2 =" ║            ╚════╗  "
    fs =" ║ " # 7 # # # # # #                
    f3 ="  ╚════════════════╝  "
    lst = [f1,f2]+[fs+('{:^'+str(w)+'}').format(name[w*i:w*(i+1)])+fs for i in range(h-1)]+[f3] 
    return lst
    

kek = [" 1*** ", " 2*** ", " 3*** ", " 4*** "]

def createGrid(folderLst, screen):
    _, w = screen.getmaxyx() 
    h = 16
    oneFolder = folderLst[0]
    nWidth = max([len(el) for el in oneFolder])
    nHeight = len(oneFolder) 
    nW = w // nWidth 
    #nH = h // nHeight 
    
    hc = 0
    spacer = 0
    for c in range(0, len(folderLst)+1, nW):
        lineFolders = folderLst[c:c+nW]
        fLines = []
        for i in range(nHeight):
            fLines.append('')
            for f in lineFolders:
                fLines[i] += (f[i]) 
                

        for i, line in enumerate(fLines):
            out = ('{:^' + str(w) + '}').format(line)
            screen.addstr(hc*nHeight + i + spacer, 0, out)

        spacer += 1
        hc += 1


class Element:
    def __init__(self, name):
        self.name = name
        self.width = 22
        self.height = 10 
        self.x = 0
        self.y = 0

class Controller:
    def __init__(self):
        self.curses, self.screen = init()
        self.height, self.width = self.screen.getmaxyx()
        self.c = 0
        self.elements = []
        self.dir = "" 

    def add(self, name):
        e = Element(name)
        self.elements.append(e)
        print(name)
        self.c += 1

    def collision(self):
        space = 0
        oneEl = self.elements[0]
        sideSpace = (self.width % oneEl.width)//2
        nH = self.height // oneEl.height
        nW = self.width // oneEl.width
        
        h = 0
        for c in range(0, len(self.elements), nW):
            line = self.elements[c:c+nW]
            
            for w, el in enumerate(line):
                el.x = sideSpace + w*el.width
                el.y = h*el.height + space

            space += 1
            h += 1
                

        for el in self.elements:
            fieldX = { i for i in range(el.x, el.x+el.width+1)}
            fieldY = { j for j in range(el.y, el.y+el.height+1)}
            el.field = (fieldX, fieldY)


    
    def print(self):
        createGrid( [folder(el.name) for el in self.elements], self.screen)
    
    def check(self, x, y):
        for el in self.elements:
            if x in el.field[0] and y in el.field[1]:
                return el 
        return None

    def clear(self):
        self.c = 0
        self.elements = []

def cmd(arg):
    ls = s.check_output(arg).decode("utf-8").split('\n')
    ss = [ el for el in ls if el != '' ] 
    return ss 

def show(c):
    c.screen.clear()
    if c.dir != "":
        os.chdir(c.dir)
    folders = cmd(["ls", "-a"])

    for el in folders:
        c.add(el)
        c.print()
        c.collision()
    c.screen.refresh()
    whait(c)


def whait(c):
    while True:
        event = c.screen.getch() 
        if event == ord("q"): break
        if event == c.curses.KEY_MOUSE:
            _, mx, my, _, _ = c.curses.getmouse()
            el = c.check(mx, my)
            if el != None and os.path.isdir(el.name):
               c.dir = el.name
               c.clear()
               show(c)
            c.screen.refresh()
    exit(c.curses)

def main():
    c = Controller()
    try:
        show(c)
    except Exception as e:
        exit(c.curses)
        print(e)
main()
