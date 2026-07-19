const logger = require('../services/logger.service');

function errorHandler(error, _req, res, _next) {
    const statusCode = error.statusCode || 500;
    const publicMessage = statusCode >= 500 ? 'Internal server error' : error.message;

    logger.error('Request failed', {
        message: error.message,
        statusCode
    });

    res.status(statusCode).json({
        error: publicMessage
    });
}

module.exports = errorHandler;
