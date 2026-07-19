const express = require('express');
const AdminController = require('../controllers/admin.controller');
const adminAuth = require('../middlewares/auth.middleware');
const asyncHandler = require('../middlewares/async-handler');

const router = express.Router();

router.get(
    '/admin/financial-report',
    adminAuth,
    asyncHandler(async (_req, res) => {
        const report = await AdminController.getFinancialReport();
        res.status(200).json(report);
    })
);

module.exports = router;
