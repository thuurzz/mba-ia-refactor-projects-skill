import sqlite3

from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DB_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def initialize_database():
    db = get_db()
    cursor = db.cursor()
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT DEFAULT '',
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            ativo INTEGER DEFAULT 1,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT DEFAULT 'cliente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pendente',
            total REAL NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT
        );

        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY(pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
            FOREIGN KEY(produto_id) REFERENCES produtos(id) ON DELETE RESTRICT
        );
        """
    )
    db.commit()

    _upgrade_legacy_passwords(cursor)
    _seed_products(cursor)
    _seed_users(cursor)
    db.commit()


def _upgrade_legacy_passwords(cursor):
    rows = cursor.execute("SELECT id, senha FROM usuarios").fetchall()
    for row in rows:
        password_value = row["senha"]
        if password_value and not _looks_like_password_hash(password_value):
            cursor.execute(
                "UPDATE usuarios SET senha = ? WHERE id = ?",
                (generate_password_hash(password_value), row["id"]),
            )


def _looks_like_password_hash(value):
    return value.startswith("scrypt:") or value.startswith("pbkdf2:")


def _seed_products(cursor):
    count = cursor.execute("SELECT COUNT(*) AS total FROM produtos").fetchone()["total"]
    if count:
        return

    products = [
        ("Notebook Gamer", "Notebook potente para jogos", 5999.99, 10, "informatica"),
        ("Mouse Wireless", "Mouse sem fio ergonomico", 89.90, 50, "informatica"),
        ("Teclado Mecanico", "Teclado mecanico RGB", 299.90, 30, "informatica"),
        ("Monitor 27", "Monitor 27 polegadas 144hz", 1899.90, 15, "informatica"),
        ("Headset Gamer", "Headset com microfone", 199.90, 25, "informatica"),
        ("Cadeira Gamer", "Cadeira ergonomica", 1299.90, 8, "moveis"),
        ("Webcam HD", "Webcam 1080p", 249.90, 20, "informatica"),
        ("Hub USB", "Hub USB 3.0 7 portas", 79.90, 40, "informatica"),
        ("SSD 1TB", "SSD NVMe 1TB", 449.90, 35, "informatica"),
        ("Camiseta Dev", "Camiseta estampa codigo", 59.90, 100, "vestuario"),
    ]
    cursor.executemany(
        """
        INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
        VALUES (?, ?, ?, ?, ?)
        """,
        products,
    )


def _seed_users(cursor):
    count = cursor.execute("SELECT COUNT(*) AS total FROM usuarios").fetchone()["total"]
    if count:
        return

    users = [
        ("Admin", "admin@loja.com", generate_password_hash("admin123"), "admin"),
        ("Joao Silva", "joao@email.com", generate_password_hash("123456"), "cliente"),
        ("Maria Santos", "maria@email.com", generate_password_hash("senha123"), "cliente"),
    ]
    cursor.executemany(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        users,
    )
