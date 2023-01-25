import { execSync } from 'child_process';
import * as fs from 'fs';

const validGradients: string[] = [
    "none",
    "autumn",
    "bone",
    "jet",
    "winter",
    "rainbow",
    "ocean",
    "summer",
    "spring",
    "cool",
    "hsv",
    "pink",
    "hot",
    "parula",
    "magma",
    "inferno",
    "plasma",
    "viridis",
    "cividis",
    "deepgreen"
];

interface IFlag {
    // the background image of the vaporwave image
    background?: string;
    
    // the misc image of the vaporwave image
    misc?: string;
    // the misc image's x position
    miscPosX?: number;
    // the misc image's y position
    miscPosY?: number;
    // the misc image's scale
    miscScale?: number;
    // the misc image's rotation
    miscRotate?: number;

    // the character image of the vaporwave image (required)
    characterPath: string;
    // the character image's x position
    characterXPos?: Number;
    // the character image's y position
    characterYPos?: number;
    // the character image's scale
    characterScale?: number;
    // the character image's rotation
    characterRotate?: number;
    // the character image's glitch value
    characterGlitch?: number;
    // the character image's glitch seed value
    characterGlitchSeed?: number;
    // the character image's gradient value accorded to cvt color gradients maps
    characterGradient?: string;


    // crt effect on the vaporwave image
    crt?: boolean;

    // output path of the vaporwave image
    outputPath?: fs.PathLike;
};

type DefaultValues = Pick<IFlag, 'characterPath' | 'miscPosX' | 'miscPosY' | 'miscScale' | 'miscRotate' | 'characterYPos' | 'characterXPos' | 'characterScale' | 'crt' | 'outputPath' | 'characterGlitch' | 'characterRotate' | 'characterGlitchSeed'>;
const defaultFlag: DefaultValues = {
    characterPath: '',
    miscPosX: 0,
    miscPosY: 0,
    miscScale: 100,
    miscRotate: 0,
    characterXPos: 0,
    characterYPos: 0,
    characterScale: 100,
    characterRotate: 0,
    characterGlitch: .1,
    characterGlitchSeed: 0,
    crt: false,
    outputPath: "./output/vaporwave.png"
};

const vaporwaver = (flags: IFlag = defaultFlag) => {

    // check if the background path is valid
    if (!flags.background) flags.background = "default";
    if (!fs.existsSync('./picts/backgrounds/' + flags.background + '.png'))
        throw new Error("Background path is not valid.");

    // check if the path of character file exists
    if (!fs.existsSync(flags.characterPath))
        throw new Error("Character path is not valid.");

    // check if the character is a png file according to the base64 header
    if (fs.readFileSync(flags.characterPath).toString('base64').slice(0, 8) !== 'iVBORw0K')
        throw new Error("Character file is not a png file.");

    // if gradient is specified, check if it is valid
    flags.characterGradient = flags.characterGradient?.toLocaleLowerCase();
    if (flags.characterGradient && !validGradients.includes(flags.characterGradient))
        throw new Error("Gradient is not valid.");
    
    // if misc is specified, check if it exists
    if (flags.misc && !fs.existsSync('./picts/miscs' + flags.misc + '.png'))
        throw new Error("Misc path is not valid.");

    // if background is specified, check if it exists
    if (flags.background && !fs.existsSync('./picts/backgrounds' + flags.background + '.png'))
        throw new Error("Background path is not valid.");
    
    // check if the output path is valid
    if (flags.outputPath && !fs.existsSync(flags.outputPath))
        throw new Error("Output path is not valid.");

    // check if miscposx and miscposy are between -100 and 100
    if (flags.miscPosX && (flags.miscPosX < -100 || flags.miscPosX > 100))
        throw new Error("Misc X position is not valid. The value must be between -100 and 100.");

    if (flags.miscPosY && (flags.miscPosY < -100 || flags.miscPosY > 100))
        throw new Error("Misc Y position is not valid. The value must be between -100 and 100.");

    // check if miscscale is between 1 and 200
    if (flags.miscScale && (flags.miscScale < 1 || flags.miscScale > 200))
        throw new Error("Misc scale value is not valid. The value must be between 1 and 200.");
    
    // check if miscrotate is between -360 and 360
    if (flags.miscRotate && (flags.miscRotate < -360 || flags.miscRotate > 360))
        throw new Error("Misc rotate value is not valid. The value must be between -360 and 360.");

    // check if characterxpos and characterypos are between -100 and 100
    if (flags.characterXPos && (flags.characterXPos < -100 || flags.characterXPos > 100))
        throw new Error("Character X position is not valid. The value must be between -100 and 100.");
    
    if (flags.characterYPos && (flags.characterYPos < -100 || flags.characterYPos > 100))
        throw new Error("Character Y position is not valid. The value must be between -100 and 100.");

    // check if characterscale is between 1 and 200
    if (flags.characterScale && (flags.characterScale < 1 || flags.characterScale > 200))
        throw new Error("Character scale value is not valid. The value must be between 1 and 200.");
    
    // check if characterrotate is between -360 and 360
    if (flags.characterRotate && (flags.characterRotate < -360 || flags.characterRotate > 360))
        throw new Error("Character rotate value is not valid. The value must be between -360 and 360.");

    // check if characterglitch is between .1 and 10
    if (flags.characterGlitch && (flags.characterGlitch < .1 || flags.characterGlitch > 10))
        throw new Error("Character glitch value is not valid. The value must be between .1 and 10.");
    
    // check if characterglitchseed is between 0 and 100
    if (flags.characterGlitchSeed && (flags.characterGlitchSeed < 0 || flags.characterGlitchSeed > 100))
        throw new Error("Character glitch seed value is not valid. The value must be between 0 and 100.");

    // execute a python script to generate the vaporwave image
    try {
        execSync(`python3 ./vaporwaver.py 
            -b=${flags.background}
            -c=${flags.characterPath}
            -m=${flags.misc || ''}
            -mx=${flags.miscPosX || 0}
            -my=${flags.miscPosY || 0}
            -ms=${flags.miscScale || 100}
            -mr=${flags.miscRotate || 0}
            -cx=${flags.characterXPos || 0}
            -cy=${flags.characterYPos || 0}
            -cs=${flags.characterScale || 100}
            -cr=${flags.characterRotate || 0}
            -cg=${flags.characterGlitch || .1}
            -cgs=${flags.characterGlitchSeed || 0}
            -cgd=${flags.characterGradient || 'none'}
            -crt=${flags.crt || false}
            -o=${flags.outputPath || './output/vaporwave.png'}`
        );
    } catch (e: any) {
        // throw an error if the python script fails to execute and print the error
        throw new Error(e.stderr.toString());
    };
};

export default vaporwaver;