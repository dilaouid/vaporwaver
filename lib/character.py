from data import globals, gui

def moveCharacter(axis, value):
    globals["val"][axis] = value
    print(globals["character"], globals["val"]["characterXpos"], globals["val"]["characterYpos"])
    gui["frame"]["canvas"].coords(globals["character"], globals["val"]["characterXpos"], globals["val"]["characterYpos"])