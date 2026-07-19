const database = require('../config/database');

class EnrollmentModel {
    static async create(userId, courseId) {
        const result = await database.run(
            'INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)',
            [userId, courseId]
        );

        return {
            id: result.lastID,
            userId,
            courseId
        };
    }
}

module.exports = EnrollmentModel;
