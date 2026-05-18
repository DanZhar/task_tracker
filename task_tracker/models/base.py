"""Абстрактный базовый класс задачи Task."""

import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from task_tracker.enums import VALID_TRANSITIONS, Priority, Status
from task_tracker.exceptions import InvalidStatusTransitionError, ValidationError
from task_tracker.interfaces import Displayable, Serializable
from task_tracker.mixins import HistoryMixin, TimestampMixin


class Task(Serializable, Displayable, ABC, TimestampMixin, HistoryMixin):
    """Абстрактный базовый класс задачи.

    Поля:
        id (str): уникальный идентификатор (UUID4)
        title (str): название задачи (3–128 символов, через property)
        description (str): описание задачи
        _status (Status): текущий статус (защищённое поле)
        priority (Priority): приоритет
        assignee (User | None): исполнитель
        created_at (datetime): дата создания
        updated_at (datetime): дата последнего изменения

    Абстрактные методы (реализуются в наследниках):
        estimate() -> float: оценка трудоёмкости в часах
        label() -> str: строковая метка типа ([BUG], [FEATURE], [EPIC])

    Магические методы (нужно реализовать):
        __str__: [LABEL] #id_short — title (PRIORITY)
        __repr__: ClassName(id='...', title='...', status=STATUS)
        __eq__, __hash__: сравнение и хеширование по id
        __lt__, __le__, __gt__, __ge__: сравнение по priority (для сортировки)

    Инкапсуляция:
        - status доступен только на чтение (через @property)
        - изменение статуса — только через change_status()
        - title валидируется через property setter (3–128 символов)
    """

    def __init__(
            self,
            title: str,
            description: str = "",
            priority: Priority = Priority.MEDIUM,
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self._status = Status.OPEN
        self.priority = priority
        self.assignee = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # ── title property ──────────────────────────────────────────────

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        # Валидация длины (3–128 символов).
        # При невалидном значении выбрасывайте ValidationError.

        if not isinstance(value, str):
            raise ValidationError("Title must be a string")

        if len(value) < 3 or len(value) > 128:
            raise ValidationError("Title length must be from 3 to 128 symbols")

        self._title = value

    # ── status property ─────────────────────────────────────────────

    @property
    def status(self) -> Status:
        return self._status

    def change_status(self, new_status: Status) -> None:
        """Изменить статус задачи с проверкой допустимости перехода.

        Допустимые переходы определены в enums.VALID_TRANSITIONS.
        При недопустимом переходе — InvalidStatusTransitionError.
        При изменении — обновить updated_at и записать в историю (HistoryMixin).

        Args:
            new_status: новый статус
        """

        if new_status not in VALID_TRANSITIONS[self.status]:
            raise InvalidStatusTransitionError("Invalid status transition.")

        self._record_transition(self._status, new_status)
        self._status = new_status

    # ── абстрактные методы ──────────────────────────────────────────

    @abstractmethod
    def estimate(self) -> float:
        """Оценка трудоёмкости в часах. Зависит от типа задачи."""
        ...

    @abstractmethod
    def label(self) -> str:
        """Строковая метка типа задачи: [BUG], [FEATURE], [EPIC]."""
        ...

    # ── Serializable ────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Сериализовать задачу в словарь.

        Должен включать поле "type" ("bug", "feature", "epic"),
        assignee_id вместо объекта User, даты в ISO 8601.
        """
        task_type = type(self).__name__.lower()

        return {
            "type": task_type,
            "id": self.id,
            "title": self._title,
            "description": self.description,
            "status": self._status.value,
            "priority": self.priority.value,
            "assignee_id": self.assignee.id if self.assignee is not None else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Создать задачу из словаря. Выбор класса по полю 'type'."""

        from task_tracker.models.tasks import Bug, Epic, Feature

        task_type = data.get("type")
        if task_type == "bug":
            return Bug.from_dict(data)
        elif task_type == "feature":
            return Feature.from_dict(data)
        elif task_type == "epic":
            return Epic.from_dict(data)
        else:
            raise ValueError(f"Unknown task type: '{task_type}'")

    def _restore_fields(self, data: dict) -> None:
        self.id = data["id"]
        self._status = Status(data["status"])
        self.created_at = datetime.fromisoformat(data["created_at"])
        self.assignee = None
        self._assignee_id = data.get("assignee_id")
        self._history = data.get("history", [])

        self.updated_at = datetime.fromisoformat(data["updated_at"])

    # ── Displayable ─────────────────────────────────────────────────

    def short_display(self) -> str:
        """Краткое представление: [LABEL] title — PRIORITY — STATUS"""

        return f"{self.label()} {self._title} — {self.priority.name} — {self._status.name}"

    def full_display(self) -> str:
        """Полное представление со всеми полями."""

        return "\n".join(self._display_lines())

    def _display_lines(self) -> list[str]:
        assignee_str = self.assignee.short_display() if self.assignee else "–"
        lines = [
            f"{self.label()} {self.title}",
            f"  ID       : {self.id}",
            f"  Status   : {self.status.name}",
            f"  Priority : {self.priority.name}",
            f"  Assignee : {assignee_str}",
            f"  Created  : {self.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"  Updated  : {self.updated_at.strftime('%Y-%m-%d %H:%M')}",
            f"  Estimate : {self.estimate():.1f}h",
        ]
        if self.description:
            lines.append(f"  Desc     : {self.description}")
        if self.history:
            lines.append("  History  :")
            for log in self.history:
                lines.append(f"    {log['at']}  {log['from']} → {log['to']}")
        return lines

    # ── Магические методы ───────────────────────
    # __str__:  [BUG] #abc12 — Fix login (HIGH)
    def __str__(self):
        return f"{self.label()} #{self.id[:8]} — {self._title} ({self.priority})"

    # __repr__: Bug(id='abc12', title='Fix login', status=OPEN)
    def __repr__(self) -> str:
        return (f"{type(self).__name__}(id={self.id!r}, "
                f"title={self._title!r}, "
                f"status={self._status.name})")

    # __eq__, __hash__: по id
    def __eq__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented

        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    # __lt__, __le__, __gt__, __ge__: по priority.value
    def __lt__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented

        return self.priority.value < other.priority.value

    def __le__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented

        return self.priority.value <= other.priority.value

    def __gt__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented

        return self.priority.value > other.priority.value

    def __ge__(self, other) -> bool:
        if not isinstance(other, Task):
            return NotImplemented

        return self.priority.value >= other.priority.value
