const crypto = require('crypto');

const KEY_LENGTH = 64;
const SALT_LENGTH = 16;
const WORK_FACTOR = 16384;

class PasswordService {
    static hash(password) {
        const salt = crypto.randomBytes(SALT_LENGTH).toString('hex');
        const derivedKey = crypto.scryptSync(password, salt, KEY_LENGTH, {
            N: WORK_FACTOR
        });

        return `${salt}:${derivedKey.toString('hex')}`;
    }
}

module.exports = PasswordService;
