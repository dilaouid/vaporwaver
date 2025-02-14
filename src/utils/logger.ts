import { writeFileSync, appendFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

export class Logger {
    private static instance: Logger;
    private logFile: string;
    private debugMode: boolean;

    private constructor() {
        const rootDir = dirname(fileURLToPath(import.meta.url));
        const logsDir = join(rootDir, '..', '..', 'logs');

        // Ensure logs directory exists
        if (!existsSync(logsDir)) {
            mkdirSync(logsDir, { recursive: true });
        }

        this.logFile = join(logsDir, 'vaporwaver.log');
        this.debugMode = process.env.VAPORWAVER_DEBUG === 'true';

        // Initialize log file
        if (!existsSync(this.logFile)) {
            writeFileSync(this.logFile, '');
        }
    }

    static getInstance(): Logger {
        if (!Logger.instance) {
            Logger.instance = new Logger();
        }
        return Logger.instance;
    }

    private formatMessage(level: string, message: string, meta?: any): string {
        const timestamp = new Date().toISOString();
        const metaStr = meta ? `\n${JSON.stringify(meta, null, 2)}` : '';
        return `[${timestamp}] ${level}: ${message}${metaStr}\n`;
    }

    private log(level: string, message: string, meta?: any): void {
        const formattedMessage = this.formatMessage(level, message, meta);
        appendFileSync(this.logFile, formattedMessage);

        if (this.debugMode || level === 'ERROR') {
            console.log(formattedMessage);
        }
    }

    info(message: string, meta?: any): void {
        this.log('INFO', message, meta);
    }

    warn(message: string, meta?: any): void {
        this.log('WARN', message, meta);
    }

    error(message: string, meta?: any): void {
        this.log('ERROR', message, meta);
    }

    debug(message: string, meta?: any): void {
        if (this.debugMode) {
            this.log('DEBUG', message, meta);
        }
    }

    clearLogs(): void {
        writeFileSync(this.logFile, '');
    }

    setDebugMode(enabled: boolean): void {
        this.debugMode = enabled;
    }
}

export const logger = Logger.getInstance();
