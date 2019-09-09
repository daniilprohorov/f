
import curses
import os
import subprocess as s

mmask = curses.ALL_MOUSE_EVENTS
screen = curses.initscr()
curses.curs_set(0)
screen.keypad(1)
curses.mousemask(mmask)
curses.noecho()
class Element:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        fieldX = { i for i in range(x, x+width+1)}
        fieldY = { j for j in range(y, y+height+1)}
        self.field = (fieldX, fieldY)

class Controller:
    c = 0
    elements = []
    dir = ""

    def __init__(self):
        pass

    def add(self, name):
        e = Element(name, 0, self.c, len(name), 0)
        self.elements.append(e)
        print(name)
        screen.addstr(self.c, 0, name)
        self.c += 1
    
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
    screen.clear()
    if c.dir != "":
        os.chdir(c.dir)
    folders = cmd(["ls", "-a"])

    for el in folders:
        c.add(el)

    screen.refresh()
    whait(c)


def whait(c):
    while True:
        event = screen.getch() 
        if event == ord("q"): break
        if event == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            y, x = screen.getyx()
            el = c.check(mx, my)
            if el != None and os.path.isdir(el.name):
               c.dir = el.name
               c.clear()
               show(c)
            screen.refresh()

    curses.endwin()

c = Controller()
show(c)
print("Window ended.")
