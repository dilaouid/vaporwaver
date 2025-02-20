import { spawn } from 'child_process';
import { existsSync, promises as fs } from 'fs';
import path, { join, dirname } from 'path';
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
    characterOnly?: boolean;
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

        const rootPath = join(dirname(fileURLToPath(import.meta.url)), '..');

        // Validate paths and files - modifié pour supprimer .png si présent
        const cleanBackgroundName = typeof flags.background === 'string' 
            ? flags.background.replace(/\.png$/, '')
            : 'default';
            
        const cleanMiscName = typeof flags.misc === 'string'
            ? flags.misc.replace(/\.png$/, '')
            : 'none';

        const bgPath = cleanBackgroundName.includes(path.sep)
            ? flags.background as string
            : join(rootPath, 'picts', 'backgrounds', `${cleanBackgroundName}.png`);

        const miscPath = cleanMiscName.includes(path.sep)
            ? flags.misc as string
            : join(rootPath, 'picts', 'miscs', `${cleanMiscName}.png`);

        const pyScript = join(rootPath, 'vaporwaver.py');

        // Si on est en mode characterOnly, on valide seulement le chemin du personnage
        const requiredFiles: Array<{ path: PathLike, name: string }> = [
            { path: flags.characterPath, name: 'Character' },
            { path: pyScript, name: 'Python script' }
        ];

        // Only validate background and misc if we're not in characterOnly mode
        if (!flags.characterOnly) {
            requiredFiles.push({ path: bgPath, name: 'Background' });
            if (miscPath && cleanMiscName !== 'none') {
                requiredFiles.push({ path: miscPath, name: 'Misc' });
            }
        }

        for (const file of requiredFiles) {
            if (!existsSync(file.path)) {
                throw new VaporwaverError(`${file.name} file not found: ${file.path}`);
            }
            if (file.path.toString().endsWith('.png') && !await isValidPngFile(file.path.toString())) {
                throw new VaporwaverError(`Invalid PNG file: ${file.path}`);
            }
        }
        
        const pyArgs = [pyScript];
        
        // Arguments communs toujours requis
        pyArgs.push(
            `-c=${flags.characterPath}`,
            `-o=${flags.outputPath ?? join(rootPath, 'tmp', 'output.png')}`
        );
        
        if (flags.characterOnly) {
            // En mode characterOnly, ne passer que les paramètres nécessaires
            pyArgs.push(
                `--character-only`,
                `-cgd=${flags.characterGradient?.toLowerCase() ?? 'none'}`,
                `-cg=${flags.characterGlitch ?? 0.1}`,
                `-cgs=${flags.characterGlitchSeed ?? 0}`
            );
        } else {
            // En mode normal, passer tous les paramètres
            if (flags.crt === true) {
                pyArgs.push("-crt");
            }
            
            pyArgs.push(
                `-b=${cleanBackgroundName}`,
                `-m=${cleanMiscName}`,
                `-cx=${flags.characterXPos ?? 0}`,
                `-cy=${flags.characterYPos ?? 0}`,
                `-cs=${flags.characterScale ?? 100}`,
                `-cr=${flags.characterRotate ?? 0}`,
                `-cg=${flags.characterGlitch ?? 0.1}`,
                `-cgs=${flags.characterGlitchSeed ?? 0}`,
                `-cgd=${flags.characterGradient?.toLowerCase() ?? 'none'}`,
                `-mx=${flags.miscPosX ?? 0}`,
                `-my=${flags.miscPosY ?? 0}`,
                `-ms=${flags.miscScale ?? 100}`,
                `-mr=${flags.miscRotate ?? 0}`
            );
        }

        logger.debug('Executing Python script with args:', { pyArgs });

        // Execute Python script
        return new Promise((resolve, reject) => {
            const pythonProcess = spawn('python', pyArgs, {
                env: {
                    ...process.env,
                    PYTHONPATH: rootPath
                }
            });

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