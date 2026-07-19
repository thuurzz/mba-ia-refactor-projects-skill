const database = require('../config/database');

class CourseModel {
    static async findActiveById(courseId) {
        return database.get(
            'SELECT id, title, price, active FROM courses WHERE id = ? AND active = 1',
            [courseId]
        );
    }
}

module.exports = CourseModel;
