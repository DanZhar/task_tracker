"""Перечисления: Status, Priority, Role и допустимые переходы статусов."""

from enum import Enum


class Status(Enum):
    """Статусы задачи."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CLOSED = "closed"


class Priority(Enum):
    """Приоритеты задачи (числовые значения для сортировки)."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Role(Enum):
    """Роли пользователей."""

    DEVELOPER = "developer"
    QA = "qa"
    TEAM_LEAD = "team_lead"
    PM = "pm"


# Допустимые переходы между статусами.
# Ключ — текущий статус, значение — множество допустимых следующих статусов.
VALID_TRANSITIONS: dict[Status, set[Status]] = {
    Status.OPEN: {Status.IN_PROGRESS},
    Status.IN_PROGRESS: {Status.IN_REVIEW, Status.OPEN},
    Status.IN_REVIEW: {Status.DONE, Status.IN_PROGRESS},
    Status.DONE: {Status.CLOSED, Status.IN_PROGRESS},
    Status.CLOSED: set(),  # терминальный статус
}
