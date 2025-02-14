import { vaporwaver, VaporwaverError } from '../vaporwaver.js';

describe('vaporwaver', () => {
    it('should throw error for invalid character path', async () => {
        await expect(vaporwaver({
            characterPath: 'nonexistent.png'
        })).rejects.toThrow(VaporwaverError);
    });
});
