import pygame

def cleanup(bodytext):
    print(type(bodytext))
    # stuff for autosaving and cleanup would go here when implemented
    print("text on screen at close time:")

    last_index = len(bodytext) - 1
    for i, line in enumerate(bodytext):
            if not line.endswith("\n"):
                line += "\n"
            bodytext[i] = line
            bodytext[i] = line if line.endswith("\n") else line + "\n"
    joined_bodytext = ''.join(bodytext)
    print(joined_bodytext)

    pygame.quit()