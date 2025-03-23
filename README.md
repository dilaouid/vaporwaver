<h1 align="center">vaporwaver</h1>
<p align="center"><i>Python version of existing <a target="_blank" href="https://github.com/dilaouid/vaporwaver">vaporwaver</a> PHP version</i></p>
<hr>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) ![NPM](https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)


# Python usage
A Python3 script to create vaporwave image based on PNG files. An improved version of the PHP one I did 2 years ago. However, this time I used multiple third-party libraries, which are:
- PIL (Pillow)
- glitch-this (https://github.com/TotallyNotChase/glitch-this)
- opencv-python

You can install them with `pip install -r requirements.txt`.

![example](https://github.com/dilaouid/vaporwaver.py/blob/media/example.png)

<hr>

This program uses **tkinter** for the GUI tool (very pretty)

## How does it works
The program takes an image, with or without transparency (though, please use an image with transparency for a better result!), we will call this image the "character"
You can move the character in the X and Y axis, and scale it. You can apply a glitch amount and seed on it and also a predefined gradient map filter.
The gradients are the built in opencv colormap

![colormap](https://github.com/dilaouid/vaporwaver.py/blob/media/gradients.png)

You can add a predefined misc item behind the character, which you can :
- Move
- Rotate
- Scale

And you can select one of the predefined background image. The output image will have a size of 460 x 595 px

## Image ressources
⚠️ **WARNING** ⚠️

For launching, this program needs three files in specific paths. They are already in the repository, but please do not rename nor delete them. You can replace their content tho.
- `picts/backgrounds/default.png`
- `picts/crt/crt.png`
- `picts/miscs/none.png`

**Do not remove thoses files, at any cost !**

### Backgrounds
The backgrounds size, in order to be selectable in the GUI list, must have the size of the output image, which means 460 x 595 px. You can name them as you want, they must be `PNG` files located at the `picts/backgrounds` folder.

### Miscs
The miscs items are just decorations to put behind the character. There is no specific restriction on it. You can take any size, but they still musts be `PNG` files.

## What does the program looks like ?
![screenshot](https://github.com/dilaouid/vaporwaver.py/blob/media/screenshot.png)

## CLI mode
You can also use this program with the CLI. Fill the correct arguments to create your vaporwavec image. You can have more informations with `py vaporwaver.py -h`
Here is the correct usage:
```
usage: vaporwaver.py [-h] [-b background] [-m misc] [-mx miscPosX] [-my miscPosY] [-ms miscScale] [-mr miscRotate] [-c characterPath] [-cx characterXpos] [-cy characterYpos]
                     [-cs characterScale] [-cr characterRotation] [-cg characterGlitch] [-cgs characterGlitchSeed] [-cgd characterGradient] [-cgl characterGlow] [-crt crt] [--characterOnly] [-o output]

Vaporwave image editor

optional arguments:
  -h, --help            show this help message and exit
  -b                    Background image name for the vaporwaver render (without extension) in picts/backgrounds/ folder (default: default)
  -m                    Misc image name for the vaporwaver render (without extension) in picts/miscs/ folder (default: none)
  -mx                   Misc X position (default: 0) [-100, 100]
  -my                   Misc Y position (default: 0) [-100, 100]
  -ms                   Misc scale (default: 100) [1, 200]
  -mr                   Misc rotation (default: 0) [-360, 360]
  -c                    Character image path for the vaporwaver render (default: none) [REQUIRED]
  -cx                   Character X position (default: 0) [-100, 100]
  -cy                   Character Y position (default: 0) [-100, 100]
  -cs                   Character scale (default: 100) [1, 200]
  -cr                   Character rotation (default: 0) [-360, 360]
  -cg                   Character glitch (default: 0.1) [0.1, 1]
  -cgs                  Character glitch seed (default: 1) [0, 100]
  -cgd                  Character gradient to apply, cvt colormap name (default: none) [none, autumn, bone, jet, winter, rainbow, ocean, summer, spring, cool, hsv, pink, hot, parula, magma, inferno, plasma, viridis, cividis, deepgreen]
  -cgl                  Character glow to apply (default: none) [none, red, green, blue, yellow]
  -crt                  CRT effect (default: False)
  --characterOnly       Export only the character with applied effects (no background/misc)
  -o                    Output file name with path (default: output.png) PNG format only
```


# TypeScript usage

Install the package using either npm or pnpm:
```bash
npm install vaporwaver-ts
# or
pnpm install vaporwaver-ts
```

The package will automatically attempt to install the required Python dependencies during installation. You can manually check the dependencies by running:
```bash
npx check-vaporwaver
```

Import and use the package:
```typescript
import { vaporwaver } from "vaporwaver-ts";

// Example usage
await vaporwaver({
    background: "neon",          // One of the predefined backgrounds in picts/backgrounds/
    misc: "diamonds",           // One of the predefined misc items in picts/miscs/
    characterPath: "./my-character.png",  // Path to your character PNG file
    characterGradient: "plasma", // Optional: apply a gradient effect
    outputPath: "./output.png"  // Where to save the result
});

// Export only the character with effects (no background or misc items)
await vaporwaver({
    characterPath: "./my-character.png",
    characterGradient: "plasma",
    characterGlitch: 2.5,
    characterOnly: true,         // Export only the character with applied effects
    outputPath: "./character-only.png"
});
```

## Configuration (IFlag interface)
```typescript
interface IFlag {
    background?: string;        // Name of background file (without .png) from picts/backgrounds/
    misc?: string;             // Name of misc file (without .png) from picts/miscs/
    miscPosX?: number;         // [-100, 100] X position of misc
    miscPosY?: number;         // [-100, 100] Y position of misc
    miscScale?: number;        // [1, 200] Scale of misc
    miscRotate?: number;       // [-360, 360] Rotation of misc
    characterPath: string;     // Path to character PNG file (required)
    characterXPos?: number;    // [-100, 100] X position of character
    characterYPos?: number;    // [-100, 100] Y position of character
    characterScale?: number;   // [1, 200] Scale of character
    characterRotate?: number;  // [-360, 360] Rotation of character
    characterGlitch?: number;  // [0.1, 10] Glitch effect intensity
    characterGlitchSeed?: number; // [0, 100] Seed for glitch effect
    characterGradient?: GradientType; // Predefined gradient type
    crt?: boolean;            // Apply CRT effect
    outputPath?: string;      // Output file path (PNG)
    characterOnly?: boolean;  // Export only the character with effects (no background/misc)
}
```

## Available gradients
The following gradient types are available for `characterGradient`:
- none, autumn, bone, jet, winter, rainbow, ocean
- summer, spring, cool, hsv, pink, hot, parula
- magma, inferno, plasma, viridis, cividis, deepgreen

## Requirements
- Node.js ≥ 14.0.0
- Python ≥ 3.7.0

## Debug Mode
Set `VAPORWAVER_DEBUG=true` environment variable to enable debug logging.

## Error Handling
The library now includes comprehensive error handling:
- VaporwaverError: Custom error class with detailed error information
- Validation errors for all input parameters
- PNG file validation
- Path security checks

## Logging
Logs are stored in the `logs` directory by default:
- INFO: General operation information
- WARN: Non-critical warnings
- ERROR: Critical errors
- DEBUG: Detailed debug information (when debug mode is enabled)

## Development
```bash
# Install dependencies
npm install

# Build
npm run build

# Run tests
npm run test

# Check Python dependencies
npm run check-deps

# Format code
npm run format

# Lint code
npm run lint
```

## Troubleshooting
Common issues and solutions:

1. Python dependency installation fails
    - Try running pip install --user -r requirements.txt
    - Check Python version (>= 3.7.0 required)
2. File not found errors
    - Ensure all required files exist in the correct directories
    - Check file permissions
3. PNG validation fails
    - Ensure input files are valid PNG format
    - Check file permissions
