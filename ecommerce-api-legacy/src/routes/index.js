const adminRoutes = require('./admin.routes');
const checkoutRoutes = require('./checkout.routes');
const userRoutes = require('./user.routes');

function registerRoutes(app) {
    app.use('/api', checkoutRoutes);
    app.use('/api', adminRoutes);
    app.use('/api', userRoutes);
}

module.exports = registerRoutes;
