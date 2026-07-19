from werkzeug.security import check_password_hash, generate_password_hash


class AuthService:
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password, password_hash):
        if not password_hash.startswith(("scrypt:", "pbkdf2:")):
            return False
        return check_password_hash(password_hash, password)
