import re

from src.middlewares.error_handler import BadRequestError


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 200


def validate_product_payload(payload, valid_categories):
    if not payload:
        raise BadRequestError("Dados invalidos")

    nome = str(payload.get("nome", "")).strip()
    descricao = str(payload.get("descricao", "")).strip()
    preco = payload.get("preco")
    estoque = payload.get("estoque")
    categoria = payload.get("categoria", "geral")

    if not nome:
        raise BadRequestError("Nome e obrigatorio")
    if len(nome) < MIN_NAME_LENGTH:
        raise BadRequestError("Nome muito curto")
    if len(nome) > MAX_NAME_LENGTH:
        raise BadRequestError("Nome muito longo")
    if categoria not in valid_categories:
        raise BadRequestError("Categoria invalida")
    if not isinstance(estoque, int):
        raise BadRequestError("Estoque deve ser um inteiro")
    if not isinstance(preco, (int, float)):
        raise BadRequestError("Preco deve ser numerico")
    if preco < 0:
        raise BadRequestError("Preco nao pode ser negativo")
    if estoque < 0:
        raise BadRequestError("Estoque nao pode ser negativo")

    return {
        "nome": nome,
        "descricao": descricao,
        "preco": float(preco),
        "estoque": estoque,
        "categoria": categoria,
    }


def validate_user_payload(payload):
    if not payload:
        raise BadRequestError("Dados invalidos")

    nome = str(payload.get("nome", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    senha = payload.get("senha", "")

    if not nome or not email or not senha:
        raise BadRequestError("Nome, email e senha sao obrigatorios")
    if len(nome) < MIN_NAME_LENGTH:
        raise BadRequestError("Nome muito curto")
    if not EMAIL_PATTERN.match(email):
        raise BadRequestError("Email invalido")
    if len(senha) < 6:
        raise BadRequestError("Senha deve ter pelo menos 6 caracteres")

    return {"nome": nome, "email": email, "senha": senha}
