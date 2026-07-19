const { config } = require('../config');
const HttpError = require('../services/http-error');

function extractToken(authorizationHeader) {
    if (!authorizationHeader) {
        return null;
    }

    if (authorizationHeader.startsWith('Bearer ')) {
        return authorizationHeader.slice('Bearer '.length).trim();
    }

    return authorizationHeader.trim();
}

function adminAuth(req, _res, next) {
    const headerToken = req.get('x-admin-token');
    const bearerToken = extractToken(req.get('authorization'));
    const providedToken = headerToken || bearerToken;

    if (!providedToken || providedToken !== config.adminToken) {
        next(new HttpError(401, 'Unauthorized'));
        return;
    }

    next();
}

module.exports = adminAuth;
