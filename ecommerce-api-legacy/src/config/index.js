function requireConfig(name) {
    const value = process.env[name];

    if (!value) {
        throw new Error(`Missing required environment variable: ${name}`);
    }

    return value;
}

const config = {
    adminToken: requireConfig('ADMIN_TOKEN'),
    dbName: process.env.DB_NAME || ':memory:',
    nodeEnv: process.env.NODE_ENV || 'development',
    port: Number(process.env.PORT || 3000),
    seedUserEmail: process.env.SEED_USER_EMAIL || 'leonan@fullcycle.com.br',
    seedUserName: process.env.SEED_USER_NAME || 'Leonan',
    seedUserPassword: process.env.SEED_USER_PASSWORD || '123'
};

module.exports = {
    config
};
