BANKS = [
    "etaonrishdlfcm",
    "uwgpbyvkjxqz.,",
    '!?-/()&"\'\n ',
]
ALLCHARS = ''.join(BANKS)
CODES = [
    "onecap",
    "lower",
    "upper",
    "digit"
]

#from components.fourbitencoding import tinyify, bigify
from components.janitor import cleanup
import pygame


dimensions = {
    "WIDTH": 800,
    "HEIGHT": 600,
    "LEFTMARGIN": 100,
    "RIGHTMARGIN": 100,
    "MARGINWIDTHSPACE": 600,
    "UPPERMARGIN": 100,
    "LOWERMARGIN": 100,
    "LINEPADDING": 4,
    "BORDER": 10,
    "FONTSIZE": 25
}

colours = {
    "white": (255, 255, 255),
    "grey": (128, 128, 128),
    "dark_grey": (64, 64, 64),
    "black": (0, 0, 0)
}

def wraplines(lines, font, dimensions=dimensions):
    wrappedlines = []
    for line in lines:
        words = line.split(" ")
        thisline = []
        for i, word in enumerate(words):

            if font.size(word)[0] > dimensions["MARGINWIDTHSPACE"]:       # if the line has a single word that is too long to fit in the margins
                print("word too long")
                segments = []                               # create a list to store the segments of the word 
                thissegment = []                            # create a list to store the characters of the current segment
                for char in word:                                                   # iterate through the characters in the word                                
                    thissegment.append(char)                                        # add the character to the current segment
                    if font.size("".join(thissegment))[0] > dimensions[ "MARGINWIDTHSPACE"]:       # check if its now too long to fit in the margins
                        thissegment.pop()                                           # remove the last character if it is
                        segments.append(''.join(thissegment))                       # add this segment to the list of segments
                        thissegment = [char]                                # start a new segment with the current character
                segments.append(''.join(thissegment))                       # add the last segment to the list of segments
                print(segments)
                words[i:i+1] = segments                                     # replace the word with the list of segments
                print(words)
                continue

        for i, word in enumerate(words):

            thisline.append(word)
            if font.size(" ".join(thisline))[0] > dimensions[ "MARGINWIDTHSPACE"]:  # if the line is too long to fit in the margins
                thisline.pop()                                       # remove the last word
                if thisline:
                    wrappedlines.append(" ".join(thisline))
                thisline = [word]
        wrappedlines.append(" ".join(thisline))
    return wrappedlines

def handleinput(event):
    

    keypressed = False

    def backspace():
        if bodytext == []:                              # if there are no lines in the body text
            return                                      # do nothing
        lastline = bodytext[len(bodytext)-1]            # get the last line of the body text
        lastlinelength = len(lastline) - 1              # get the length of the last line
        if lastlinelength == -1:                        # if the last line is empty
            bodytext.pop()                              # remove the last line (kind of like removing a \n character)
        else:                                           # if the last line is not empty
            bodytext[len(bodytext)-1] = lastline[:-1]   # remove the last character from the last line

    def returnkey():
        bodytext.append("")                     # add a new line to the body text list

    def keyboardinput():
        if bodytext == []:                              # if there are no lines in the body text
            bodytext.append("")                         # add a new line
        bodytext[len(bodytext)-1] += event.unicode      # add the keyboard input to the last line


    if event.type == pygame.KEYDOWN:
        keypressed = True
        if event.key == pygame.K_RETURN:            # on enter
            returnkey()
        elif event.key == pygame.K_BACKSPACE:               # on backspace
            backspace()                                     
        else:                                               # if any other key is pressed
            keyboardinput()
    return keypressed




def renderbodytext(bodytext, scrollpos, window, pagecolour=colours["dark_grey"], textcolour=colours["white"], linepadding=4):
    lineheight = dimensions["UPPERMARGIN"] + scrollpos
    MARGINWIDTHSPACE = dimensions["MARGINWIDTHSPACE"]
    LEFTMARGIN = dimensions["LEFTMARGIN"]
    UPPERMARGIN = dimensions["UPPERMARGIN"]


                
    def renderline(line, y, colour):
        linesurf = font.render(line, True, colour)          # put the line into a surface
        window.blit(linesurf, (LEFTMARGIN, y))              # blit the surface to the window at the desired height

    pygame.draw.rect(window, pagecolour, (LEFTMARGIN-10, UPPERMARGIN-10 + scrollpos, MARGINWIDTHSPACE+20, 5000))
    
    for i, line in enumerate(bodytext):
        renderline(line, lineheight, textcolour)
        lineheight += fontsize + linepadding
                

    # lineheight = 50 + scrollpos
    # if bodytext == [] or bodytext == [""]:
    #     bodytextsurf = font.render("input...", True, grey)
    #     window.blit(bodytextsurf, (100, lineheight))
    # for i, line in enumerate(bodytext):
    #     if i == len(bodytext) - 1:
    #         islastline = True
    #     else: 
    #         islastline = False
    #     bodytextsurf = font.render(line + ("<" if cursorvisible and islastline else ""), True, white)
    #     window.blit(bodytextsurf, (100, lineheight))
    #     lineheight += fontsize + linepadding




pygame.init()



window = pygame.display.set_mode((dimensions["WIDTH"], dimensions["HEIGHT"]))
pygame.display.set_caption("TinyLETTERS")


fontname = pygame.font.match_font("consolas")
fontsize = 25
font = pygame.font.Font(fontname, fontsize)
linepadding = 4
cursortimer = 0
pygame.key.set_repeat(300, 50)


bodytext = ["test"]
bodytextsurf = None
cursorvisible = True
scrollpos = 0

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)                                  # limit the frame rate to 60 FPS

    cursortimer += 1                                # increment the cursor timer once per frame
    if cursortimer > 30:                            # every 30 frames (0.5 seconds)
        cursorvisible = not cursorvisible           # toggle the cursor visibility
        cursortimer = 0                             # reset the timer

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            keypressed = handleinput(event)             # handle the input event (returns true if a key was pressed, false otherwise)
            if keypressed:
                cursorvisible = True
                cursortimer = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:                       # scroll up
                scrollpos += 10
            elif event.button == 5:                     # scroll down
                scrollpos -= 10

    window.fill(colours["black"])
    if scrollpos > 0:
        scrollpos = 0
    bodytext = wraplines(bodytext, font)
    renderbodytext(bodytext, scrollpos, window, linepadding=linepadding)

    pygame.display.flip()
cleanup(bodytext)           # perform closing operations (save, cleanup, etc.)
        