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
        self.screen.bkgd(' ', self.curses.COLOR_BLACK)
        self.height, self.width = self.screen.getmaxyx()
        self.c = 0
        self.elements = []
        self.dir = "" 

        self.pos = 0
        self.pad = None
        self.padHeight = 0 

    def padRefresh(self, move):
        self.pos += move 
        #  self.pad.refresh(self.pos, 0, 0, 0, self.padHeight, self.width)
        self.pad.refresh(self.pos, 0, 0, 0, self.height - 1, self.width)


    def add(self, name):
        e = Element(name)
        self.elements.append(e)
        self.c += 1


    
    def print(self):

        screenW = self.width
        folderW = self.elements[0].width
        folderH = self.elements[0].height
        nW      = screenW // folderW 
        sideSpace = screenW % folderW 
        els = self.elements
        elCount = len(els)
        sideSpaceL = sideSpace // 2
        y = 0
        self.padHeight = ((elCount // nW) + 1)*(folderH + 1)
        self.pad = self.curses.newpad(self.padHeight, screenW)
        self.padRefresh(0)
        #  self.pad = self.curses.newpad(1000, screenW)
        self.pad.scrollok(True)
        for i in range(0, elCount, nW):
            localY = 0
            for c, el in enumerate(els[i: i + nW]):
                localY = 0
                el.y = y                    
                el.x = sideSpaceL + c*folderW
                for line in folder(el.name):
                    self.pad.addstr(el.y+localY, el.x, line)
                    #  self.pad.addstr(0, 0, "1")
                    #  self.pad.addstr(1, 0, "2")
                    localY += 1
            y += localY + 1

        self.screen.refresh()
        self.padRefresh(0)

    def check(self, x, y):
        #  self.screen.addstr( 25, 0, str(x) + " " + str(y))
        for el in self.elements:
            xLim = el.x + el.width
            yLim = el.y + el.height
            if (el.x <= x <= xLim and el.y <= y <= yLim):
                return el 
        return None

    def clear(self):
        self.c = 0
        self.elements = []
        self.pos = 0
        self.pad = None
        self.padHeight = 0 

def cmd(arg):
    ls = s.check_output(arg).decode("utf-8").split('\n')
    ss = [ el for el in ls if el != '' ] 
    return ss 

def show(c):
    c.clear()
    c.screen.clear()
    if c.dir != "":
        os.chdir(c.dir)
    folders = cmd(["ls", "-a"])

    for el in folders:
        c.add(el)
    c.print()
    #  c.padRefresh(0)
    whait(c)


def whait(c):
    while True:
        event = c.screen.getch() 
        if event == ord("q"): break

        #  c.screen.addstr(2, 0, str(event))
        #  if event == 409:
        #      _, mx, my, _, bs = c.curses.getmouse()

        if event == c.curses.KEY_MOUSE:
            _, mx, my, _, bs = c.curses.getmouse()

            #  c.screen.addstr(2, 0, str(bs))

            if bs == c.curses.BUTTON1_CLICKED:
                el = c.check(mx, my)
                if el != None and os.path.isdir(el.name):
                    c.dir = el.name

                    show(c)
                    c.screen.refresh()
            elif bs == c.curses.BUTTON4_PRESSED:
                c.padRefresh(1)
            elif bs == 2097152:
                c.padRefresh(-1)


            #  elif bs == c.curses.BUTTON_SHIFT:
            #      c.padRefresh(-1)
    exit(c.curses)

def main():
    c = Controller()
#    try:
    show(c)
#    except Exception as e:
#        exit(c.curses)
#        print(e)
main()
