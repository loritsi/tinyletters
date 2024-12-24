import pygame

def cleanup(bodytext):
    # stuff for autosaving and cleanup would go here when implemented
    print("text on screen at close time:")

    for i, line in enumerate(bodytext):
        if i != len(bodytext) - 1:
            bodytext[i] = line if line.endswith("\n") else line + "\n"
    joined_bodytext = ''.join(bodytext)
    print(joined_bodytext)

    pygame.quit()