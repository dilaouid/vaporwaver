import { spawn } from 'child_process';
import { existsSync, promises as fs } from 'fs';
import path, { join, dirname, extname } from 'path';
import { fileURLToPath } from 'url';
import type { PathLike } from 'fs';
import { DependencyChecker } from './utils/dependency-checker';
import { logger } from './utils/logger';

export const validGradients = [
    "none", "autumn", "bone", "jet", "winter", "rainbow", "ocean",
    "summer", "spring", "cool", "hsv", "pink", "hot", "parula",
    "magma", "inferno", "plasma", "viridis", "cividis", "deepgreen"
] as const;

export type GradientType = typeof validGradients[number];

export interface IFlag {
    background?: string | PathLike;
    misc?: string | PathLike;
    miscPosX?: number;
    miscPosY?: number;
    miscScale?: number;
    miscRotate?: number;
    characterPath: string;
    characterXPos?: number;
    characterYPos?: number;
    characterScale?: number;
    characterRotate?: number;
    characterGlitch?: number;
    characterGlitchSeed?: number;
    characterGradient?: GradientType;
    crt?: boolean;
    outputPath?: PathLike;
}

export class VaporwaverError extends Error {
    constructor(message: string, public readonly details: any = {}) {
        super(message);
        this.name = 'VaporwaverError';
    }
}

const isValidPngFile = async (filePath: string): Promise<boolean> => {
    try {
        const buffer = await fs.readFile(filePath, { flag: 'r' });
        return buffer.length >= 8 &&
            buffer[0] === 0x89 &&
            buffer[1] === 0x50 &&
            buffer[2] === 0x4E &&
            buffer[3] === 0x47;
    } catch {
        return false;
    }
};

export async function vaporwaver(flags: IFlag): Promise<void> {
    logger.info('Starting vaporwaver process', { flags });

    try {
        // Check dependencies first
        await DependencyChecker.checkPython();
        await DependencyChecker.checkPythonDependencies();

        const rootPath = dirname(fileURLToPath(import.meta.url));

        // Validate paths and files
        const bgPath = typeof flags.background === 'string' && !flags.background.includes(path.sep) 
            ? join(rootPath, 'picts', 'backgrounds', `${flags.background}.png`)
            : flags.background || join(rootPath, 'picts', 'backgrounds', 'default.png');

        const miscPath = typeof flags.misc === 'string' && !flags.misc.includes(path.sep)
            ? join(rootPath, 'picts', 'miscs', `${flags.misc}.png`)
            : flags.misc || join(rootPath, 'picts', 'miscs', 'none.png');

        const pyScript = join(rootPath, 'vaporwaver.py');

        // Validate required files
        const requiredFiles = [
            { path: bgPath, name: 'Background' },
            { path: flags.characterPath, name: 'Character' },
            { path: pyScript, name: 'Python script' }
        ];

        if (miscPath && flags.misc !== 'none') {
            requiredFiles.push({ path: miscPath, name: 'Misc' });
        }

        for (const file of requiredFiles) {
            if (!existsSync(file.path)) {
                throw new VaporwaverError(`${file.name} file not found: ${file.path}`);
            }
            if (file.path.toString().endsWith('.png') && !await isValidPngFile(file.path.toString())) {
                throw new VaporwaverError(`Invalid PNG file: ${file.path}`);
            }
        }

        // Validate output path
        if (flags.outputPath) {
            const outputExt = extname(flags.outputPath.toString()).toLowerCase();
            if (outputExt !== '.png') {
                throw new VaporwaverError('Output file must be a PNG file');
            }
            if (flags.outputPath.toString().includes('..') || flags.outputPath.toString().includes('&')) {
                throw new VaporwaverError('Invalid output path');
            }
        }

        // Validate numeric parameters
        const validations = [
            { value: flags.miscPosX, min: -100, max: 100, name: "Misc X position" },
            { value: flags.miscPosY, min: -100, max: 100, name: "Misc Y position" },
            { value: flags.miscScale, min: 1, max: 200, name: "Misc scale" },
            { value: flags.miscRotate, min: -360, max: 360, name: "Misc rotation" },
            { value: flags.characterXPos, min: -100, max: 100, name: "Character X position" },
            { value: flags.characterYPos, min: -100, max: 100, name: "Character Y position" },
            { value: flags.characterScale, min: 1, max: 200, name: "Character scale" },
            { value: flags.characterRotate, min: -360, max: 360, name: "Character rotation" },
            { value: flags.characterGlitch, min: 0.1, max: 10, name: "Character glitch" },
            { value: flags.characterGlitchSeed, min: 0, max: 100, name: "Character glitch seed" }
        ];

        for (const validation of validations) {
            if (validation.value !== undefined &&
                (validation.value < validation.min || validation.value > validation.max)) {
                throw new VaporwaverError(
                    `${validation.name} must be between ${validation.min} and ${validation.max}`
                );
            }
        }

        // Validate gradient
        if (flags.characterGradient &&
            !validGradients.includes(flags.characterGradient.toLowerCase() as GradientType)) {
            throw new VaporwaverError(
                `Invalid gradient type. Must be one of: ${validGradients.join(', ')}`
            );
        }

        // Prepare Python arguments
        const pyArgs = [
            pyScript,
            `-b=${flags.background || 'default'}`,
            `-c=${flags.characterPath}`,
            `-m=${flags.misc || 'none'}`,
            `-mx=${flags.miscPosX ?? 0}`,
            `-my=${flags.miscPosY ?? 0}`,
            `-ms=${flags.miscScale ?? 100}`,
            `-mr=${flags.miscRotate ?? 0}`,
            `-cx=${flags.characterXPos ?? 0}`,
            `-cy=${flags.characterYPos ?? 0}`,
            `-cs=${flags.characterScale ?? 100}`,
            `-cr=${flags.characterRotate ?? 0}`,
            `-cg=${flags.characterGlitch ?? 0.1}`,
            `-cgs=${flags.characterGlitchSeed ?? 0}`,
            `-cgd=${flags.characterGradient?.toLowerCase() ?? 'none'}`,
            `-crt=${flags.crt ?? false}`,
            `-o=${flags.outputPath ?? join(rootPath, 'tmp', 'output.png')}`
        ];

        logger.debug('Executing Python script with args:', { pyArgs });

        // Execute Python script
        return new Promise((resolve, reject) => {
            const pythonProcess = spawn('python', pyArgs);
            let stderrData = '';

            pythonProcess.stdout.on('data', (data: Buffer) => {
                logger.debug('Python stdout:', data.toString());
            });

            pythonProcess.stderr.on('data', (data: Buffer) => {
                stderrData += data;
                logger.error('Python stderr:', data.toString());
            });

            pythonProcess.on('close', (code) => {
                if (code === 0) {
                    logger.info('Vaporwaver process completed successfully');
                    resolve();
                } else {
                    const error = new VaporwaverError(
                        `Python process failed with code ${code}`,
                        { stderr: stderrData }
                    );
                    logger.error('Vaporwaver process failed', error);
                    reject(error);
                }
            });

            pythonProcess.on('error', (err) => {
                const error = new VaporwaverError(
                    'Failed to start Python process',
                    { originalError: err }
                );
                logger.error('Process start failed', error);
                reject(error);
            });
        });
    } catch (error) {
        logger.error('Vaporwaver error:', error);
        throw error instanceof VaporwaverError ? error : new VaporwaverError(
            'An unexpected error occurred',
            { originalError: error }
        );
    }
}