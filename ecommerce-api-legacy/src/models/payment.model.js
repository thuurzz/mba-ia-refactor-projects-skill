const database = require('../config/database');

class PaymentModel {
    static async create(enrollmentId, amount, status) {
        const result = await database.run(
            'INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)',
            [enrollmentId, amount, status]
        );

        return {
            amount,
            enrollmentId,
            id: result.lastID,
            status
        };
    }
}

module.exports = PaymentModel;
