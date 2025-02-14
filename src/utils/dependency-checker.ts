import { spawn } from "child_process";

export class DependencyError extends Error {
    constructor(message: string, public readonly details: any = {}) {
        super(message);
        this.name = 'DependencyError';
    }
}

export class DependencyChecker {
    private static pythonCommand = process.platform === 'win32' ? 'python' : 'python3';
    private static pipCommand = process.platform === 'win32' ? 'pip' : 'pip3';

    static async checkPython(minVersion = '3.7.0'): Promise<void> {
        try {
            const version = await this.getPythonVersion();
            if (!this.isVersionSatisfied(version, minVersion)) {
                throw new DependencyError(
                    `Python version ${minVersion} or higher is required. Found: ${version}`
                );
            }
        } catch (error) {
            if (error instanceof DependencyError) throw error;
            throw new DependencyError('Python is not installed or not accessible');
        }
    }

    static async checkPythonDependencies(): Promise<void> {
        try {
            const deps = await this.getInstalledPythonPackages();
            const required = ['Pillow', 'glitch-this', 'opencv-python'];
            const missing = required.filter(dep => !deps.some(installed => 
                installed.toLowerCase().startsWith(dep.toLowerCase())
            ));

            if (missing.length > 0) {
                // Try to install missing dependencies
                await this.installMissingDependencies(missing);
            }
        } catch (error) {
            throw new DependencyError(
                'Failed to verify Python dependencies',
                { originalError: error }
            );
        }
    }

    private static async getPythonVersion(): Promise<string> {
        return new Promise((resolve, reject) => {
            const python = spawn(this.pythonCommand, ['--version']);
            let output = '';

            python.stdout.on('data', (data) => { output += data; });
            python.stderr.on('data', (data) => { output += data; });

            python.on('close', (code) => {
                if (code === 0) {
                    const version = output.match(/(\d+\.\d+\.\d+)/);
                    if (version) {
                        resolve(version[1]);
                    } else {
                        reject(new Error('Could not parse Python version'));
                    }
                } else {
                    reject(new Error(`Python check failed with code ${code}`));
                }
            });
        });
    }

    private static async getInstalledPythonPackages(): Promise<string[]> {
        return new Promise((resolve, reject) => {
            const pip = spawn(this.pipCommand, ['freeze']);
            let output = '';

            pip.stdout.on('data', (data) => { output += data; });
            pip.stderr.on('data', (data) => { /* ignore stderr */ });

            pip.on('close', (code) => {
                if (code === 0) {
                    resolve(output.split('\n').filter(Boolean));
                } else {
                    reject(new Error('Failed to get installed packages'));
                }
            });
        });
    }

    private static async installMissingDependencies(packages: string[]): Promise<void> {
        // Try different installation methods
        const methods = [
            { cmd: this.pipCommand, args: ['install', '--user'] },
            { cmd: this.pipCommand, args: ['install'] },
            { cmd: this.pythonCommand, args: ['-m', 'pip', 'install', '--user'] },
            { cmd: this.pythonCommand, args: ['-m', 'pip', 'install'] }
        ];

        for (const method of methods) {
            try {
                await this.tryInstallMethod(method.cmd, [...method.args, ...packages]);
                return; // Installation successful
            } catch (error) {
                console.warn(`Installation attempt failed with method ${method.cmd}`, error);
                // Continue to next method
            }
        }

        throw new DependencyError(
            'Failed to install Python dependencies. Please install manually:\n' +
            `${this.pythonCommand} -m pip install ${packages.join(' ')}`
        );
    }

    private static async tryInstallMethod(cmd: string, args: string[]): Promise<void> {
        return new Promise((resolve, reject) => {
            const install = spawn(cmd, args);
            let output = '';

            install.stdout.on('data', (data) => { output += data; });
            install.stderr.on('data', (data) => { output += data; });

            install.on('close', (code) => {
                if (code === 0) {
                    resolve();
                } else {
                    reject(new Error(`Installation failed with code ${code}\n${output}`));
                }
            });
        });
    }

    private static isVersionSatisfied(current: string, required: string): boolean {
        const parseVersion = (v: string): number[] => v.split('.').map(Number);
        const [currentMajor, currentMinor, currentPatch] = parseVersion(current);
        const [reqMajor, reqMinor, reqPatch] = parseVersion(required);

        if (currentMajor !== reqMajor) return currentMajor > reqMajor;
        if (currentMinor !== reqMinor) return currentMinor > reqMinor;
        return currentPatch >= reqPatch;
    }
}
