import sys, os
from data import globals
import argparse

from lib.output import outputPicture

infos = {
    "background": {
        "description": "Background image name for the vaporwaver render (without extension) in picts/backgrounds/ folder (default: default)",
        "flag": "-b",
    },
    "misc": {
        "description": "Misc image name for the vaporwaver render (without extension) in picts/miscs/ folder (default: none)",
        "flag": "-m"
    },
    "miscPosX": {
        "description": "Misc X position (default: 0) [-100, 100]",
        "flag": "-mx",
        "range": [-100, 100]
    },
    "miscPosY": {
        "description": "Misc Y position (default: 0) [-100, 100]",
        "flag": "-my",
        "range": [-100, 100]
    },
    "miscScale": {
        "description": "Misc scale (default: 100) [1, 200]",
        "flag": "-ms",
        "range": [1, 200]
    },
    "miscRotate": {
        "description": "Misc rotation (default: 0) [-360, 360]",
        "flag": "-mr",
        "range": [-360, 360]
    },
    "characterPath": {
        "description": "Character image path for the vaporwaver render (default: none) [REQUIRED]",
        "flag": "-c"
    },
    "characterXpos": {
        "description": "Character X position (default: 0) [-100, 100]",
        "flag": "-cx",
        "range": [-100, 100]
    },
    "characterYpos": {
        "description": "Character Y position (default: 0) [-100, 100]",
        "flag": "-cy",
        "range": [-100, 100]
    },
    "characterScale": {
        "description": "Character scale (default: 100) [1, 200]",
        "flag": "-cs",
        "range": [1, 200]
    },
    "characterRotation": {
        "description": "Character rotation (default: 0) [-360, 360]",
        "flag": "-cr",
        "range": [-360, 360]
    },
    "characterGlitch": {
        "description": "Character glitch (default: 0.1) [0.1, 1]",
        "flag": "-cg",
        "range": [0.1, 10]
    },
    "characterGlitchSeed": {
        "description": "Character glitch seed (default: 1) [0, 100]",
        "flag": "-cgs",
        "range": [0, 100]
    },
    "characterGradient": {
        "description": "Character gradient to apply, cvt colormap name (default: none) [none, autumn, bone, jet, winter, rainbow, ocean, summer, spring, cool, hsv, pink, hot, parula, magma, inferno, plasma, viridis, cividis, deepgreen]",
        "flag": "-cgd",
        "range": globals["gradients"]
    },
    "characterGlow": {
        "description": "Character glow to apply (default: none) [none, red, green, blue, yellow]",
        "flag": "-cgl",
        "range": globals["glow"]
    },
    "crt": {
        "description": "CRT effect (default: False)",
        "flag": "-crt"
    },
    "output": {
        "description": "Output file name with path (default: output.png) PNG format only",
        "flag": "-o"
    },

}

flags = {
    c: {
        "value": globals["render"][c] if c in globals["render"] else globals["render"]["val"][c],
        "type": "str" if c == "characterPath" else (  # Forcer str pour characterPath
            "bool" if c == "crt" else (  # Forcer bool pour crt
            type(globals["render"][c]).__name__ if c in globals["render"] else 
            type(globals["render"]["val"][c]).__name__ if globals["render"]["val"][c] is not None else
            "str"  # Type par défaut si la valeur est None
            )),
        "description": infos[c]["description"],
        "flag": infos[c]["flag"],
        "range": infos[c]["range"] if "range" in infos[c] else None
    } for c in infos
}

def apply_args():
    parser = argparse.ArgumentParser(description="Vaporwave image editor")
    type_mapping = { "int": int, "float": float, "str": str, "bool": bool }
    
    for c in flags:
        parser.add_argument(flags[c]["flag"], type=type_mapping[flags[c]["type"]], 
                          default=flags[c]["value"], help=flags[c]["description"], 
                          dest=c, metavar=c)
    
    args = parser.parse_args()
    
    # Nettoyage des fichiers temporaires
    if os.path.exists("tmp/char.png"):
        os.remove("tmp/char.png")
    
    for c in flags:
        value = getattr(args, c)
        
        if c == "characterPath":
            if value is None:
                sys.stderr.write("Error: characterPath is required")
                sys.exit(1)
            globals["render"]["val"]["characterPath"] = value
            if not os.path.isfile(value):
                sys.stderr.write(f"Error: Character file not found: {value}")
                sys.exit(1)

        elif c == "output" and value is not None:
            if not value.endswith(".png"):
                sys.stderr.write("Error: The output file must be a png")
                sys.exit(1)
            globals["render"]["output"] = value
        elif c == "background":
            bg_name = value if value != 'default' else 'default'
            bg_path = os.path.join('picts', 'backgrounds', f'{bg_name}.png')
            if not os.path.isfile(bg_path):
                sys.stderr.write(f"Error: Background file not found: {bg_path}")
                sys.exit(1)
            globals["render"]["background"] = bg_path
        elif c == "misc":
            misc_name = value if value != 'none' else 'none'
            misc_path = os.path.join('picts', 'miscs', f'{misc_name}.png')
            if not os.path.isfile(misc_path):
                sys.stderr.write(f"Error: Misc file not found: {misc_path}")
                sys.exit(1)
            globals["render"]["misc"] = misc_path
        else:
            param_name = c
            if c in ["characterXpos", "characterYpos", "characterScale", 
                    "characterRotation", "characterGlitch", "characterGlitchSeed",
                    "characterGradient", "characterGlow", "miscPosX", "miscPosY",
                    "miscScale", "miscRotate", "crt"]:
                globals["render"]["val"][param_name] = value
                
                # Validation des ranges
                if flags[c]["range"] is not None:
                    if c == "characterGlitch":
                        start_value, end_value = flags[c]["range"]
                        if value < start_value or value > end_value:
                            sys.stderr.write(f"Error: {c} must be in {flags[c]['range']}")
                            sys.exit(1)
                    elif c in ["characterGradient", "characterGlow"]:
                        if value not in flags[c]["range"]:
                            sys.stderr.write(f"Error: {c} must be in {flags[c]['range']}")
                            sys.exit(1)
                    elif ((value not in flags[c]["range"]) and 
                          (value not in range(flags[c]["range"][0], flags[c]["range"][1] + 1))):
                        sys.stderr.write(f"Error: {c} must be in {flags[c]['range']}")
                        sys.exit(1)

    if not os.path.isfile(globals["render"]["background"]):
        sys.stderr.write(f"Error: Background file not found: {globals['render']['background']}")
        sys.exit(1)
        
    if globals["render"]["misc"] != "none" and not os.path.isfile(globals["render"]["misc"]):
        sys.stderr.write(f"Error: Misc file not found: {globals['render']['misc']}")
        sys.exit(1)
        
    if not os.path.isfile(globals["render"]["val"]["characterPath"]):
        sys.stderr.write(f"Error: Character file not found: {globals['render']['val']['characterPath']}")
        sys.exit(1)

    outputPicture(True)