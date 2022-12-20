import pygame, sys

mouseClicked = False

inputs = {
    "enter": False,
    "w": False,
    "a": False,
    "s": False,
    "d": False,
    "e": False,
    "f": False,
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "escape": False,
    "space": False,
    "mouseHold": False,
    "mouseClick": False,
    "mouseFinishClick": True,
    "mouseUp": False
    }


def updateInputs():
    global inputs, mouseClicked

    # Get mouse input
    inputs["mouseClick"] = False
    inputs["mouseUp"] = False
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        inputs["mouseHold"] = True
        if not(mouseClicked):
            inputs["mouseClick"] = True
            mouseClicked = True
    else:
        inputs["mouseHold"] = False
        if mouseClicked:
            inputs["mouseUp"] = True
        mouseClicked = False

    inputs["enter"] = False

    # Get key input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                inputs["a"] = True
            if event.key == pygame.K_f:
                inputs["f"] = True
            if event.key == pygame.K_RETURN:
                inputs["enter"] = True
            if event.key == pygame.K_s:
                inputs["s"] = True
            if event.key == pygame.K_d:
                inputs["d"] = True
            if event.key == pygame.K_w:
                inputs["w"] = True
            if event.key == pygame.K_SPACE:
                inputs["space"] = True
            if event.key == pygame.K_UP:
                inputs["up"] = True
            if event.key == pygame.K_DOWN:
                inputs["down"] = True
            if event.key == pygame.K_LEFT:
                inputs["left"] = True
            if event.key == pygame.K_RIGHT:
                inputs["right"] = True
            if event.key == pygame.K_ESCAPE:
                inputs["escape"] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                inputs["a"] = False
            if event.key == pygame.K_s:
                inputs["s"] = False
            if event.key == pygame.K_f:
                inputs["f"] = False
            if event.key == pygame.K_d:
                inputs["d"] = False
            if event.key == pygame.K_w:
                inputs["w"] = False
            if event.key == pygame.K_SPACE:
                inputs["space"] = False
            if event.key == pygame.K_UP:
                inputs["up"] = False
            if event.key == pygame.K_DOWN:
                inputs["down"] = False
            if event.key == pygame.K_LEFT:
                inputs["left"] = False
            if event.key == pygame.K_RIGHT:
                inputs["right"] = False
            if event.key == pygame.K_ESCAPE:
                inputs["escape"] = False

