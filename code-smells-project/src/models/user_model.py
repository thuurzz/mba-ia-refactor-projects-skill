import sqlite3

from src.middlewares.error_handler import ConflictError
from src.models.database import get_db


class UserModel:
    @staticmethod
    def get_all():
        rows = get_db().execute(
            "SELECT id, nome, email, tipo, criado_em FROM usuarios ORDER BY id"
        ).fetchall()
        return [_serialize_user(row) for row in rows]

    @staticmethod
    def get_by_id(user_id):
        row = get_db().execute(
            "SELECT id, nome, email, tipo, criado_em FROM usuarios WHERE id = ?",
            (user_id,),
        ).fetchone()
        return _serialize_user(row) if row else None

    @staticmethod
    def get_auth_record_by_email(email):
        return get_db().execute(
            "SELECT id, nome, email, senha, tipo FROM usuarios WHERE email = ?",
            (email,),
        ).fetchone()

    @staticmethod
    def create(nome, email, senha, tipo="cliente"):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                (nome, email, senha, tipo),
            )
        except sqlite3.IntegrityError as error:
            raise ConflictError("Email ja cadastrado") from error
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def exists(user_id):
        row = get_db().execute(
            "SELECT 1 AS encontrado FROM usuarios WHERE id = ?",
            (user_id,),
        ).fetchone()
        return bool(row)

    @staticmethod
    def count_all():
        row = get_db().execute("SELECT COUNT(*) AS total FROM usuarios").fetchone()
        return row["total"]


def _serialize_user(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"],
        "criado_em": row["criado_em"],
    }
