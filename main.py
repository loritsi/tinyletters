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

from components import bigify
from components import tinyify
import pygame
import sys

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TinyLETTERS")

fontname = pygame.font.match_font("consolas")
fontsize = 25
font = pygame.font.Font(fontname, fontsize)
linepadding = 4
white = (255, 255, 255)
grey = (128, 128, 128)
black = (0, 0, 0)
cursortimer = 0
cursorvisible = True
pygame.key.set_repeat(300, 50)


bodytext = ["test", "test2", "test3"]
bodytextsurf = None
cursorvisible = True

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
            pygame.quit()
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:            # on enter
                bodytext.append("")                     # add a new line to the body text list
            elif event.key == pygame.K_BACKSPACE:                                   # on backspace
                if bodytext[len(bodytext)-1] != "":                                 # if the line has stuff in it
                    bodytext[len(bodytext)-1] = bodytext[len(bodytext)-1][:-1]      # remove the last character
                else:                                                               # if the line is empty
                    bodytext.pop()                                                  # just remove the line from the list entirely
            else:                                                                   # if any other key is pressed
                bodytext[len(bodytext)-1] += event.unicode                          # add the keyboard input to the last line (may result in destructive results)

    window.fill(black)

    lineheight = 50
    for line in bodytext:
        bodytextsurf = font.render(line, True, white)
        window.blit(bodytextsurf, (100, lineheight))
        lineheight += fontsize + linepadding


    pygame.display.flip()
    
        