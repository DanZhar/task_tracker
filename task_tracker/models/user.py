"""Модель пользователя."""

import uuid

from task_tracker.enums import Role
from task_tracker.interfaces import Displayable, Serializable
from task_tracker.validators import StringLengthValidator


class User(Serializable, Displayable):
    """Пользователь (участник проекта).

    Поля:
        id (str): уникальный идентификатор (UUID4)
        name (str): имя пользователя (2–64 символа, через StringLengthValidator)
        role (Role): роль в команде

    Магические методы (TODO):
        __str__: имя (роль)
        __repr__: User(id='...', name='...', role=ROLE)
        __eq__, __hash__: по id
    """

    name = StringLengthValidator(min_length=2, max_length=64)

    def __init__(self, name: str, role: Role = Role.DEVELOPER):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role

    # ── Serializable ────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Сериализовать пользователя в словарь."""
        raise NotImplementedError("TODO: Реализуйте to_dict для User")

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Создать пользователя из словаря."""
        raise NotImplementedError("TODO: Реализуйте from_dict для User")

    # ── Displayable ─────────────────────────────────────────────────

    def short_display(self) -> str:
        raise NotImplementedError("TODO: Реализуйте short_display для User")

    def full_display(self) -> str:
        raise NotImplementedError("TODO: Реализуйте full_display для User")
