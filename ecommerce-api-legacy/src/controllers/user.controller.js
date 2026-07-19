const UserModel = require('../models/user.model');
const HttpError = require('../services/http-error');

class UserController {
    static async deleteUser(userId) {
        if (!Number.isInteger(userId) || userId <= 0) {
            throw new HttpError(400, 'User id must be a positive integer');
        }

        const result = await UserModel.deleteById(userId);
        if (result.changes === 0) {
            throw new HttpError(404, 'Usuário não encontrado');
        }

        return {
            message: 'Usuário e relacionamentos removidos com sucesso.'
        };
    }
}

module.exports = UserController;
