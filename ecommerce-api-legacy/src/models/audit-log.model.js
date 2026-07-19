const database = require('../config/database');

class AuditLogModel {
    static async create(action) {
        return database.run(
            "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
            [action]
        );
    }
}

module.exports = AuditLogModel;
