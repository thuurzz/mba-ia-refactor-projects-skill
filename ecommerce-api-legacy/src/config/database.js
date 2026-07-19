const sqlite3 = require('sqlite3').verbose();
const { config } = require('./index');
const { PAYMENT_STATUS } = require('./constants');
const PasswordService = require('../services/password.service');

class Database {
    constructor() {
        this.connection = null;
    }

    connect() {
        if (this.connection) {
            return Promise.resolve(this.connection);
        }

        return new Promise((resolve, reject) => {
            this.connection = new sqlite3.Database(config.dbName, (error) => {
                if (error) {
                    reject(error);
                    return;
                }

                resolve(this.connection);
            });
        });
    }

    async initialize() {
        await this.connect();
        await this.exec('PRAGMA foreign_keys = ON');
        await this.createSchema();
        await this.seed();
    }

    async createSchema() {
        await this.exec(`
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                pass TEXT NOT NULL
            )
        `);

        await this.exec(`
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                active INTEGER NOT NULL DEFAULT 1
            )
        `);

        await this.exec(`
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        `);

        await this.exec(`
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY,
                enrollment_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE
            )
        `);

        await this.exec(`
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY,
                action TEXT NOT NULL,
                created_at DATETIME NOT NULL
            )
        `);
    }

    async seed() {
        let seededUser = await this.get(
            'SELECT id FROM users WHERE email = ?',
            [config.seedUserEmail]
        );

        if (!seededUser) {
            const hashedPassword = PasswordService.hash(config.seedUserPassword);
            const userInsert = await this.run(
                'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
                [config.seedUserName, config.seedUserEmail, hashedPassword]
            );
            seededUser = {
                id: userInsert.lastID
            };
        }

        const courseCount = await this.get('SELECT COUNT(*) AS count FROM courses');
        if (courseCount.count === 0) {
            await this.run(
                'INSERT INTO courses (title, price, active) VALUES (?, ?, ?)',
                ['Clean Architecture', 997.0, 1]
            );
            await this.run(
                'INSERT INTO courses (title, price, active) VALUES (?, ?, ?)',
                ['Docker', 497.0, 1]
            );
        }

        const enrollmentCount = await this.get(
            'SELECT COUNT(*) AS count FROM enrollments'
        );
        if (enrollmentCount.count === 0) {
            const enrollmentInsert = await this.run(
                'INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)',
                [seededUser.id, 1]
            );

            await this.run(
                'INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)',
                [enrollmentInsert.lastID, 997.0, PAYMENT_STATUS.paid]
            );
        }
    }

    run(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.connection.run(sql, params, function onRun(error) {
                if (error) {
                    reject(error);
                    return;
                }

                resolve({
                    changes: this.changes,
                    lastID: this.lastID
                });
            });
        });
    }

    get(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.connection.get(sql, params, (error, row) => {
                if (error) {
                    reject(error);
                    return;
                }

                resolve(row);
            });
        });
    }

    all(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.connection.all(sql, params, (error, rows) => {
                if (error) {
                    reject(error);
                    return;
                }

                resolve(rows);
            });
        });
    }

    exec(sql) {
        return new Promise((resolve, reject) => {
            this.connection.exec(sql, (error) => {
                if (error) {
                    reject(error);
                    return;
                }

                resolve();
            });
        });
    }
}

module.exports = new Database();
