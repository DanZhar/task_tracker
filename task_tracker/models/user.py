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

        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value
        }


    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Создать пользователя из словаря."""

        obj = cls(name=data["name"], role=Role(data["role"]))
        obj.id = data["id"]

        return obj

    # ── Displayable ─────────────────────────────────────────────────

    def short_display(self) -> str:
        return str(self)

    def full_display(self) -> str:
        return (
            f"=== Пользователь ===\n"
            f"  ID:   {self.id}\n"
            f"  Имя:  {self.name}\n"
            f"  Роль: {self.role.value}"
        )

    # ── Магические методы ───────────────────────

    def __str__(self):
        return f"{self.name} ({self.role.name})"

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, role={self.role})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return NotImplemented

        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
