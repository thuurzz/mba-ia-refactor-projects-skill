const logger = require('./logger.service');
const { PAYMENT_STATUS } = require('../config/constants');

class PaymentService {
    static process(cardNumber, amount) {
        logger.info('Payment requested', {
            amount,
            cardLast4: cardNumber.slice(-4)
        });

        const status = cardNumber.startsWith('4')
            ? PAYMENT_STATUS.paid
            : PAYMENT_STATUS.denied;

        return {
            status
        };
    }
}

module.exports = PaymentService;
