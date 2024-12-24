import pygame

def cleanup(bodytext):
    # stuff for autosaving and cleanup would go here when implemented
    print("text on screen at close time:")

    for i, line in enumerate(bodytext):
        if not i == len(bodytext) - 1:
            bodytext[i] = line + "\n" if not line.endswith("\n") else line
    bodytext = ''.join(bodytext)
    print(bodytext)

    pygame.quit()