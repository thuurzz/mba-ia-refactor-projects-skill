const express = require('express');
const UserController = require('../controllers/user.controller');
const adminAuth = require('../middlewares/auth.middleware');
const asyncHandler = require('../middlewares/async-handler');

const router = express.Router();

router.delete(
    '/users/:id',
    adminAuth,
    asyncHandler(async (req, res) => {
        const result = await UserController.deleteUser(Number(req.params.id));
        res.status(200).json(result);
    })
);

module.exports = router;
