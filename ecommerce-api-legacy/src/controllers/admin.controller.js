const ReportModel = require('../models/report.model');
const { PAYMENT_STATUS } = require('../config/constants');

class AdminController {
    static async getFinancialReport() {
        const rows = await ReportModel.getFinancialReportRows();
        const reportByCourse = new Map();

        rows.forEach((row) => {
            if (!reportByCourse.has(row.course_id)) {
                reportByCourse.set(row.course_id, {
                    course: row.course_title,
                    revenue: 0,
                    students: []
                });
            }

            const courseReport = reportByCourse.get(row.course_id);
            if (row.student_name) {
                courseReport.students.push({
                    paid: row.paid_amount,
                    student: row.student_name
                });
            }

            if (row.payment_status === PAYMENT_STATUS.paid) {
                courseReport.revenue += row.paid_amount;
            }
        });

        return Array.from(reportByCourse.values());
    }
}

module.exports = AdminController;
