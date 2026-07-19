from src.middlewares.error_handler import BadRequestError, NotFoundError
from src.models.database import get_db


class OrderModel:
    @staticmethod
    def create(user_id, items):
        db = get_db()
        cursor = db.cursor()

        product_ids = [item["produto_id"] for item in items]
        placeholders = ",".join("?" for _ in product_ids)
        product_rows = cursor.execute(
            f"SELECT * FROM produtos WHERE id IN ({placeholders})",
            tuple(product_ids),
        ).fetchall()
        products = {row["id"]: row for row in product_rows}

        total = 0
        for item in items:
            product = products.get(item["produto_id"])
            if product is None:
                raise NotFoundError(f"Produto {item['produto_id']} nao encontrado")
            if product["estoque"] < item["quantidade"]:
                raise BadRequestError(f"Estoque insuficiente para {product['nome']}")
            total += product["preco"] * item["quantidade"]

        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, ?, ?)",
            (user_id, "pendente", total),
        )
        order_id = cursor.lastrowid

        order_items = []
        stock_updates = []
        for item in items:
            product = products[item["produto_id"]]
            order_items.append(
                (order_id, item["produto_id"], item["quantidade"], product["preco"])
            )
            stock_updates.append((item["quantidade"], item["produto_id"]))

        cursor.executemany(
            """
            INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?)
            """,
            order_items,
        )
        cursor.executemany(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            stock_updates,
        )
        db.commit()
        return {"pedido_id": order_id, "total": round(total, 2)}

    @staticmethod
    def get_by_user(user_id):
        db = get_db()
        rows = db.execute(
            """
            SELECT p.id AS pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
                   ip.produto_id, ip.quantidade, ip.preco_unitario, pr.nome AS produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
            LEFT JOIN produtos pr ON pr.id = ip.produto_id
            WHERE p.usuario_id = ?
            ORDER BY p.id, ip.id
            """,
            (user_id,),
        ).fetchall()
        return _group_orders(rows)

    @staticmethod
    def get_all():
        db = get_db()
        rows = db.execute(
            """
            SELECT p.id AS pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
                   ip.produto_id, ip.quantidade, ip.preco_unitario, pr.nome AS produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
            LEFT JOIN produtos pr ON pr.id = ip.produto_id
            ORDER BY p.id, ip.id
            """
        ).fetchall()
        return _group_orders(rows)

    @staticmethod
    def update_status(order_id, status):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, order_id))
        if cursor.rowcount == 0:
            raise NotFoundError("Pedido nao encontrado")
        db.commit()

    @staticmethod
    def sales_report():
        db = get_db()
        summary = db.execute(
            """
            SELECT
                COUNT(*) AS total_pedidos,
                COALESCE(SUM(total), 0) AS faturamento,
                SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) AS pendentes,
                SUM(CASE WHEN status = 'aprovado' THEN 1 ELSE 0 END) AS aprovados,
                SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) AS cancelados
            FROM pedidos
            """
        ).fetchone()

        total_pedidos = summary["total_pedidos"]
        faturamento = summary["faturamento"]
        desconto = 0
        if faturamento > 10000:
            desconto = faturamento * 0.1
        elif faturamento > 5000:
            desconto = faturamento * 0.05
        elif faturamento > 1000:
            desconto = faturamento * 0.02

        return {
            "total_pedidos": total_pedidos,
            "faturamento_bruto": round(faturamento, 2),
            "desconto_aplicavel": round(desconto, 2),
            "faturamento_liquido": round(faturamento - desconto, 2),
            "pedidos_pendentes": summary["pendentes"] or 0,
            "pedidos_aprovados": summary["aprovados"] or 0,
            "pedidos_cancelados": summary["cancelados"] or 0,
            "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos else 0,
        }

    @staticmethod
    def count_all():
        row = get_db().execute("SELECT COUNT(*) AS total FROM pedidos").fetchone()
        return row["total"]


def _group_orders(rows):
    orders = {}
    for row in rows:
        order_id = row["pedido_id"]
        order = orders.setdefault(
            order_id,
            {
                "id": order_id,
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": [],
            },
        )
        if row["produto_id"] is not None:
            order["itens"].append(
                {
                    "produto_id": row["produto_id"],
                    "produto_nome": row["produto_nome"] or "Desconhecido",
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"],
                }
            )
    return list(orders.values())
