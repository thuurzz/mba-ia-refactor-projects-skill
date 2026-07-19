const database = require('../config/database');
const { PAYMENT_STATUS } = require('../config/constants');

class ReportModel {
    static async getFinancialReportRows() {
        return database.all(
            `
                SELECT
                    c.id AS course_id,
                    c.title AS course_title,
                    u.name AS student_name,
                    COALESCE(p.amount, 0) AS paid_amount,
                    COALESCE(p.status, ?) AS payment_status
                FROM courses c
                LEFT JOIN enrollments e ON e.course_id = c.id
                LEFT JOIN users u ON u.id = e.user_id
                LEFT JOIN payments p ON p.enrollment_id = e.id
                ORDER BY c.id, e.id
            `,
            [PAYMENT_STATUS.unpaid]
        );
    }
}

module.exports = ReportModel;
