const express = require('express');
const CheckoutController = require('../controllers/checkout.controller');
const asyncHandler = require('../middlewares/async-handler');

const router = express.Router();

router.post(
    '/checkout',
    asyncHandler(async (req, res) => {
        const result = await CheckoutController.process(req.body || {});
        res.status(200).json(result);
    })
);

module.exports = router;
