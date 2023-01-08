from data import globals, gui

def moveCharacter(axis, value):
    if globals["character"] is None:
        return
    globals["val"][axis] = value
    print(globals["character"], globals["val"]["characterXpos"], globals["val"]["characterYpos"])
    
    # change the position of the character according to % of the canvas
    gui["frame"]["canvas"].coords(globals["character"], gui["frame"]["canvas"].winfo_width() * int(globals["val"]["characterXpos"]) / 100, gui["frame"]["canvas"].winfo_height() * int(globals["val"]["characterYpos"]) / 100)