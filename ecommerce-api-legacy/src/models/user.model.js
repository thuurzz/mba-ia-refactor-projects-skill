const database = require('../config/database');

class UserModel {
    static async findByEmail(email) {
        return database.get(
            'SELECT id, name, email, pass FROM users WHERE email = ?',
            [email]
        );
    }

    static async create({ name, email, passwordHash }) {
        const result = await database.run(
            'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
            [name, email, passwordHash]
        );

        return {
            id: result.lastID,
            name,
            email
        };
    }

    static async deleteById(userId) {
        return database.run('DELETE FROM users WHERE id = ?', [userId]);
    }
}

module.exports = UserModel;
