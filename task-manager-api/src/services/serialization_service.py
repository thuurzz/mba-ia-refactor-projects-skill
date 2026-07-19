from src.services.datetime_service import ensure_utc, utc_now


def serialize_task(task):
    due_date = ensure_utc(task.due_date)
    now = utc_now()
    data = task.to_dict()
    if due_date and task.status not in {"done", "cancelled"}:
        data["overdue"] = due_date < now
    else:
        data["overdue"] = False
    data["user_name"] = task.user.name if task.user else None
    data["category_name"] = task.category.name if task.category else None
    return data


def serialize_user(user, include_tasks=False):
    data = user.to_dict()
    data["task_count"] = len(user.tasks)
    if include_tasks:
        data["tasks"] = [serialize_task(task) for task in user.tasks]
    return data


def serialize_category(category, task_count=0):
    data = category.to_dict()
    data["task_count"] = task_count
    return data
