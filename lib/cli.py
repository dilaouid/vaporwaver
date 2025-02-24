import sys, os, uuid
from data import globals
import argparse
from PIL import Image
from lib.image_handler import load_and_convert_image
from lib.output import outputPicture, OutputHandler
from lib.paths import get_asset_path

# Générer un suffixe unique pour les fichiers tmp
globals["temp_suffix"] = uuid.uuid4().hex

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
        "description": "Character image path for the vaporwaver render (REQUIRED)",
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
        "description": "Character glitch (default: 0.1) [0.1, 10]",
        "flag": "-cg",
        "range": [0.1, 10]
    },
    "characterGlitchSeed": {
        "description": "Character glitch seed (default: 1) [0, 100]",
        "flag": "-cgs",
        "range": [0, 100]
    },
    "characterGradient": {
        "description": "Character gradient to apply (default: none) [none, autumn, bone, jet, winter, rainbow, ocean, summer, spring, cool, hsv, pink, hot, parula, magma, inferno, plasma, viridis, cividis, deepgreen]",
        "flag": "-cgd",
        "range": globals["gradients"]
    },
    "crt": {
        "description": "CRT effect (default: False)",
        "flag": "-crt"
    },
    "output": {
        "description": "Output file name with path (default: output.png) PNG format only",
        "flag": "-o"
    },
    "characterOnly": {
        "description": "Export only the character with its effects without background/misc",
        "flag": "--character-only"
    },
    "miscAboveCharacter": {
        "description": "Render misc above character (default: False)",
        "flag": "--misc-above",
        "range": None
    }
}

flags = {
    c: {
        "value": globals["render"][c] if c in globals["render"] else (
            False if c in ["crt", "characterOnly", "miscAboveCharacter"] else 
            globals["render"]["val"][c] if c in globals["render"]["val"] else None
        ),
        "type": (
            "bool" if c in ["crt", "characterOnly", "miscAboveCharacter"] else
            "str" if c == "characterPath" else (
                type(globals["render"][c]).__name__ if c in globals["render"] else 
                type(globals["render"]["val"][c]).__name__ if c in globals["render"]["val"] and globals["render"]["val"][c] is not None else
                "str"
            )
        ),
        "description": infos[c]["description"],
        "flag": infos[c]["flag"],
        "range": infos[c]["range"] if "range" in infos[c] else None
    } for c in infos
}

def export_character_only(output_path):
    """Exporte uniquement le character avec ses effets (gradient, glitch)"""
    try:
        original_image = Image.open(globals["render"]["val"]["characterPath"])
        if original_image.mode != 'RGBA':
            original_image = original_image.convert('RGBA')
        if globals["render"]["val"]["characterGradient"] != "none":
            from lib.character import prepareGradientImage
            image = prepareGradientImage(original_image)
        else:
            image = original_image.copy()
        if globals["render"]["val"]["characterGlitch"] != 0.1:
            from lib.character import applyGlitchEffect
            image = applyGlitchEffect(image)
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        image.save(output_path, 'PNG')
        print(f"Character successfully exported to {output_path}")
    except Exception as e:
        sys.stderr.write(f"Error exporting character: {e}\n")
        sys.exit(1)

def apply_args():
    parser = argparse.ArgumentParser(description="Vaporwave image editor (CLI mode)")

    type_mapping = {"int": int, "float": float, "str": str, "bool": lambda x: (str(x).lower() in ['true', '1', 'yes'])}
    for c in flags:
        if flags[c]["type"] == "bool":
            parser.add_argument(flags[c]["flag"], action='store_true',
                                default=flags[c]["value"], help=flags[c]["description"],
                                dest=c)
        else:
            parser.add_argument(flags[c]["flag"], type=type_mapping[flags[c]["type"]],
                                default=flags[c]["value"], help=flags[c]["description"],
                                dest=c, metavar=c)
    args = parser.parse_args()
    globals["render"]["characterOnly"] = getattr(args, "characterOnly", False)
    value = getattr(args, "characterPath")
    if value is None:
        sys.stderr.write("Error: characterPath is required\n")
        sys.exit(1)
    
    # Définir le chemin dans les deux endroits nécessaires
    globals["render"]["characterPath"] = value
    globals["render"]["val"]["characterPath"] = value

    # Vérifier que le fichier existe et est lisible
    if not os.path.isfile(value):
        sys.stderr.write(f"Error: Character file not found: {value}\n")
        sys.exit(1)

    try:
        # Vérifier que le fichier est lisible et peut être converti
        load_and_convert_image(value)
    except Exception as e:
        sys.stderr.write(f"Error loading character file: {str(e)}\n")
        sys.exit(1)

    if not os.path.isfile(value):
        sys.stderr.write(f"Error: Character file not found: {value}\n")
        sys.exit(1)
    value = getattr(args, "output", None)
    if value is not None:
        print(f"Setting output path to: {value}")  # debug
        globals["render"]["output"] = value
        if not value.endswith(".png"):
            sys.stderr.write("Error: The output file must be a png\n")
            sys.exit(1)
    for param in ["characterGlitch", "characterGlitchSeed", "characterGradient"]:
        value = getattr(args, param, None)
        if value is not None:
            globals["render"]["val"][param] = value
            if flags[param]["range"] is not None:
                if param == "characterGlitch":
                    start_value, end_value = flags[param]["range"]
                    if value < start_value or value > end_value:
                        sys.stderr.write(f"Error: {param} must be in {flags[param]['range']}\n")
                        sys.exit(1)
                elif param == "characterGradient":
                    if value not in flags[param]["range"]:
                        sys.stderr.write(f"Error: {param} must be in {flags[param]['range']}\n")
                        sys.exit(1)
    if not globals["render"].get("characterOnly", False):
        value = getattr(args, "background", "default")
        bg_name = value if value != "default" else "default"
        bg_path = get_asset_path(os.path.join("picts", "backgrounds", f"{bg_name}.png"))
        if not os.path.isfile(bg_path):
            sys.stderr.write(f"Error: Background file not found: {bg_path}\n")
            sys.exit(1)
        globals["render"]["background"] = bg_path
        value = getattr(args, "misc", "none")
        misc_name = value if value != "none" else "none"
        misc_path = get_asset_path(os.path.join("picts", "miscs", f"{misc_name}.png"))
        if not os.path.isfile(misc_path):
            sys.stderr.write(f"Error: Misc file not found: {misc_path}\n")
            sys.exit(1)
        globals["render"]["misc"] = misc_path
        globals["misc_above_character"] = getattr(args, "miscAboveCharacter", False)
        for param in ["characterXpos", "characterYpos", "characterScale",
                      "characterRotation", "characterGlow", "miscPosX",
                      "miscPosY", "miscScale", "miscRotate", "crt"]:
            value = getattr(args, param, None)
            if value is not None:
                globals["render"]["val"][param] = value
                if param in flags and flags[param]["range"] is not None:
                    if ((value not in flags[param]["range"]) and 
                        (value not in range(flags[param]["range"][0], flags[param]["range"][1] + 1))):
                        sys.stderr.write(f"Error: {param} must be in {flags[param]['range']}\n")
                        sys.exit(1)
    if globals["render"].get("characterOnly", False):
        output_path = globals["render"].get("output", "character_output.png")
        export_character_only(output_path)
    else:
        handler = OutputHandler(cli_mode=True)
        try:
            # Initialiser le handler avec les chemins
            handler.prepare_paths()
            # Assembler l'image finale
            handler.process_image()
        except Exception as e:
            sys.stderr.write(f"Error processing image: {str(e)}\n")
            sys.exit(1)
        finally:
            handler.cleanup()

if __name__ == "__main__":
    apply_args()
