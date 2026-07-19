const express = require('express');
const { config } = require('./config');
const database = require('./config/database');
const registerRoutes = require('./routes');
const errorHandler = require('./middlewares/errorHandler');
const logger = require('./services/logger.service');

async function createApp() {
    await database.initialize();

    const app = express();
    app.use(express.json());

    registerRoutes(app);
    app.use(errorHandler);

    return app;
}

async function startServer() {
    const app = await createApp();

    return app.listen(config.port, () => {
        logger.info('Application started', {
            environment: config.nodeEnv,
            port: config.port
        });
    });
}

if (require.main === module) {
    startServer().catch((error) => {
        logger.error('Application failed to start', {
            error: error.message
        });
        process.exit(1);
    });
}

module.exports = {
    createApp,
    startServer
};
