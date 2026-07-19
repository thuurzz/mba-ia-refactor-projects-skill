import re

from src.constants import (
    DEFAULT_COLOR,
    DEFAULT_PRIORITY,
    MAX_PRIORITY,
    MAX_TITLE_LENGTH,
    MIN_PASSWORD_LENGTH,
    MIN_PRIORITY,
    MIN_TITLE_LENGTH,
    VALID_ROLES,
    VALID_STATUSES,
)
from src.errors import APIError
from src.services.datetime_service import parse_date

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$")


def _as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def validate_task_payload(data, partial=False):
    if not isinstance(data, dict) or not data:
        raise APIError("Dados inválidos", 400)

    payload = {}
    title = data.get("title")
    if title is not None:
        cleaned_title = title.strip()
        if len(cleaned_title) < MIN_TITLE_LENGTH or len(cleaned_title) > MAX_TITLE_LENGTH:
            raise APIError("Título deve ter entre 3 e 200 caracteres", 400)
        payload["title"] = cleaned_title
    elif not partial:
        raise APIError("Título é obrigatório", 400)

    if "description" in data or not partial:
        payload["description"] = data.get("description", "")

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            raise APIError("Status inválido", 400)
        payload["status"] = data["status"]
    elif not partial:
        payload["status"] = "pending"

    if "priority" in data:
        try:
            priority = int(data["priority"])
        except (TypeError, ValueError) as exc:
            raise APIError("Prioridade inválida", 400) from exc
        if priority < MIN_PRIORITY or priority > MAX_PRIORITY:
            raise APIError("Prioridade deve ser entre 1 e 5", 400)
        payload["priority"] = priority
    elif not partial:
        payload["priority"] = DEFAULT_PRIORITY

    if "user_id" in data or not partial:
        payload["user_id"] = data.get("user_id")

    if "category_id" in data or not partial:
        payload["category_id"] = data.get("category_id")

    if "due_date" in data:
        if data["due_date"]:
            try:
                payload["due_date"] = parse_date(data["due_date"])
            except ValueError as exc:
                raise APIError("Formato de data inválido. Use YYYY-MM-DD", 400) from exc
        else:
            payload["due_date"] = None

    if "tags" in data:
        tags = data["tags"]
        if isinstance(tags, list):
            payload["tags"] = ",".join(str(tag).strip() for tag in tags if str(tag).strip())
        elif tags is None:
            payload["tags"] = None
        else:
            payload["tags"] = str(tags).strip()

    return payload


def validate_user_payload(data, partial=False):
    if not isinstance(data, dict) or not data:
        raise APIError("Dados inválidos", 400)

    payload = {}

    if "name" in data:
        name = data["name"].strip()
        if not name:
            raise APIError("Nome é obrigatório", 400)
        payload["name"] = name
    elif not partial:
        raise APIError("Nome é obrigatório", 400)

    if "email" in data:
        email = data["email"].strip().lower()
        if not EMAIL_PATTERN.match(email):
            raise APIError("Email inválido", 400)
        payload["email"] = email
    elif not partial:
        raise APIError("Email é obrigatório", 400)

    if "password" in data:
        password = data["password"]
        if len(password) < MIN_PASSWORD_LENGTH:
            raise APIError("Senha deve ter no mínimo 8 caracteres", 400)
        payload["password"] = password
    elif not partial:
        raise APIError("Senha é obrigatória", 400)

    if "role" in data:
        if data["role"] not in VALID_ROLES:
            raise APIError("Role inválido", 400)
        payload["role"] = data["role"]
    elif not partial:
        payload["role"] = "user"

    if "active" in data:
        payload["active"] = _as_bool(data["active"])

    return payload


def validate_category_payload(data, partial=False):
    if not isinstance(data, dict) or not data:
        raise APIError("Dados inválidos", 400)

    payload = {}
    if "name" in data:
        name = data["name"].strip()
        if not name:
            raise APIError("Nome é obrigatório", 400)
        payload["name"] = name
    elif not partial:
        raise APIError("Nome é obrigatório", 400)

    if "description" in data or not partial:
        payload["description"] = data.get("description", "")

    if "color" in data:
        color = data["color"]
        if not isinstance(color, str) or len(color) != 7 or not color.startswith("#"):
            raise APIError("Cor inválida", 400)
        payload["color"] = color
    elif not partial:
        payload["color"] = DEFAULT_COLOR

    return payload
