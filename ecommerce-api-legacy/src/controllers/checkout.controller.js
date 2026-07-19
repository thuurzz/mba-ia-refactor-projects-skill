const AuditLogModel = require('../models/audit-log.model');
const CourseModel = require('../models/course.model');
const EnrollmentModel = require('../models/enrollment.model');
const PaymentModel = require('../models/payment.model');
const UserModel = require('../models/user.model');
const { PAYMENT_STATUS } = require('../config/constants');
const HttpError = require('../services/http-error');
const PasswordService = require('../services/password.service');
const PaymentService = require('../services/payment.service');

class CheckoutController {
    static validateInput({ userName, email, password, courseId, cardNumber }) {
        if (!userName || !email || !courseId || !cardNumber) {
            throw new HttpError(400, 'Bad Request');
        }

        if (!Number.isInteger(courseId) || courseId <= 0) {
            throw new HttpError(400, 'Course id must be a positive integer');
        }

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            throw new HttpError(400, 'Invalid email');
        }

        if (String(cardNumber).length < 13 || String(cardNumber).length > 19) {
            throw new HttpError(400, 'Invalid card number');
        }

        if (password && password.length < 6) {
            throw new HttpError(400, 'Password must have at least 6 characters');
        }
    }

    static async process(payload) {
        const requestData = {
            cardNumber: String(payload.card || ''),
            courseId: Number(payload.c_id),
            email: String(payload.eml || '').trim(),
            password: String(payload.pwd || ''),
            userName: String(payload.usr || '').trim()
        };

        CheckoutController.validateInput(requestData);

        const course = await CourseModel.findActiveById(requestData.courseId);
        if (!course) {
            throw new HttpError(404, 'Curso não encontrado');
        }

        let user = await UserModel.findByEmail(requestData.email);
        if (!user) {
            const passwordToHash = requestData.password || 'temporary-password';
            user = await UserModel.create({
                email: requestData.email,
                name: requestData.userName,
                passwordHash: PasswordService.hash(passwordToHash)
            });
        }

        const payment = PaymentService.process(requestData.cardNumber, course.price);
        if (payment.status === PAYMENT_STATUS.denied) {
            throw new HttpError(400, 'Pagamento recusado');
        }

        const enrollment = await EnrollmentModel.create(user.id, course.id);
        await PaymentModel.create(enrollment.id, course.price, payment.status);
        await AuditLogModel.create(`Checkout curso ${course.id} por ${user.id}`);

        return {
            enrollment_id: enrollment.id,
            msg: 'Sucesso'
        };
    }
}

module.exports = CheckoutController;
