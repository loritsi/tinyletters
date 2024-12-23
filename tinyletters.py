import keyboard
import sys
import os
import time
import pygetwindow as gw

TITLE = "TinyLETTERS"
os.system(f"title {TITLE}")
def is_terminal_focused():
    if gw.getActiveWindow().title == TITLE:
        return True
    else:
        return False
START_TIME = time.time()
def cursorblink():
    elapsed = int(time.time() - START_TIME)
    if elapsed % 2 == 0:
        return True
    else:
        return False

LETTERBANK = {
    "abcdefhijklmn",
    "opqrstuvwxyz."
}

class Cursor:
    INPUTMAP = {
        "up": ("line", -1),
        "down": ("line", 1),
        "enter": ("line", 1),
        "left": ("char", -1),
        "right": ("char", 1)
    }
    def __init__(self):
        self.line = 0
        self.char = 0

    def bound(self):
        linemax = len(pagetext) - 1
        charmax = len(pagetext[self.line]) - 1
        if self.line > linemax:
            self.line = linemax
        if self.char > charmax:
            self.char = charmax
        if self.line < 0:
            self.line = 0
        if self.char < 0:
            self.char = 0

    def writechar(self, input, move=True):
        if input == "space":
            input = " "
        if input == "backspace":
            self.delchar()
        if input in Cursor.INPUTMAP.keys():
            self.do(input)
        elif len(input) == 1:
            chars = list(pagetext[self.line])
            chars.insert(self.char, input)
            self.char += 1
            newline = ''.join(chars)
            pagetext[self.line] = newline
            refresh()
            self.bound()

    def delchar(self):
        linemax = len(pagetext) - 1
        charmax = len(pagetext[self.line]) - 1

    def do(self, input):
        if input.lower() in Cursor.INPUTMAP.keys():
            thismap = Cursor.INPUTMAP[input.lower()]
            setattr(self, thismap[0], getattr(self, thismap[0]) + thismap[1])
        else:
            return
        if input.lower() == "enter":
            pagetext.insert(self.line, "")
        self.bound()
        refresh()

def refresh():    
    os.system('cls' if os.name == 'nt' else 'clear')
    for i, line in enumerate(pagetext):
        if i == cursor.line:
            chars = list(line)
            chars[cursor.char] = "█"
            line = ''.join(chars)
        print(f"\t{line}")
    print(f"\nline: {cursor.line} char: {cursor.char}")
    print(f"focused: {is_terminal_focused()}")

cursor = Cursor()
pagetext = ["this is a big big big", "text document"]
refresh()
while True:
    if is_terminal_focused():
        event = keyboard.read_event()
        if event.event_type == "down":
            cursor.writechar(event.name)
        