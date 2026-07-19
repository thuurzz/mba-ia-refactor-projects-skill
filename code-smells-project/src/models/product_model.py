import sqlite3

from src.middlewares.error_handler import ConflictError
from src.models.database import get_db


class ProductModel:
    @staticmethod
    def get_all():
        rows = get_db().execute("SELECT * FROM produtos ORDER BY id").fetchall()
        return [_serialize_product(row) for row in rows]

    @staticmethod
    def get_by_id(product_id):
        row = get_db().execute(
            "SELECT * FROM produtos WHERE id = ?",
            (product_id,),
        ).fetchone()
        return _serialize_product(row) if row else None

    @staticmethod
    def create(nome, descricao, preco, estoque, categoria):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome, descricao, preco, estoque, categoria),
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update(product_id, nome, descricao, preco, estoque, categoria):
        db = get_db()
        db.execute(
            """
            UPDATE produtos
            SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ?
            WHERE id = ?
            """,
            (nome, descricao, preco, estoque, categoria, product_id),
        )
        db.commit()

    @staticmethod
    def delete(product_id):
        db = get_db()
        try:
            db.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
            db.commit()
        except sqlite3.IntegrityError as error:
            raise ConflictError("Produto possui pedidos vinculados e nao pode ser removido") from error

    @staticmethod
    def search(term, category=None, min_price=None, max_price=None):
        query = "SELECT * FROM produtos WHERE 1=1"
        params = []

        if term:
            query += " AND (nome LIKE ? OR descricao LIKE ?)"
            wildcard = f"%{term}%"
            params.extend([wildcard, wildcard])
        if category:
            query += " AND categoria = ?"
            params.append(category)
        if min_price is not None:
            query += " AND preco >= ?"
            params.append(min_price)
        if max_price is not None:
            query += " AND preco <= ?"
            params.append(max_price)

        rows = get_db().execute(query, tuple(params)).fetchall()
        return [_serialize_product(row) for row in rows]

    @staticmethod
    def count_all():
        row = get_db().execute("SELECT COUNT(*) AS total FROM produtos").fetchone()
        return row["total"]


def _serialize_product(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "descricao": row["descricao"],
        "preco": row["preco"],
        "estoque": row["estoque"],
        "categoria": row["categoria"],
        "ativo": row["ativo"],
        "criado_em": row["criado_em"],
    }
