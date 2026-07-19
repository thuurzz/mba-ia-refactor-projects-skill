function write(level, message, metadata = {}) {
    const entry = JSON.stringify({
        level,
        message,
        metadata,
        timestamp: new Date().toISOString()
    });

    process.stdout.write(`${entry}\n`);
}

module.exports = {
    error(message, metadata) {
        write('error', message, metadata);
    },
    info(message, metadata) {
        write('info', message, metadata);
    },
    warn(message, metadata) {
        write('warn', message, metadata);
    }
};
