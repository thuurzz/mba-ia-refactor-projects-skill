from datetime import UTC, datetime


def utc_now():
    return datetime.now(UTC)


def ensure_utc(value):
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=UTC)
