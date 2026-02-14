"""Абстрактный базовый класс задачи Task."""

import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from task_tracker.enums import Priority, Status
from task_tracker.interfaces import Displayable, Serializable
from task_tracker.mixins import HistoryMixin, TimestampMixin


class Task(ABC, Serializable, Displayable, TimestampMixin, HistoryMixin):
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
        self._title = title
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
        # TODO: Добавьте валидацию длины (3–128 символов).
        # При невалидном значении выбрасывайте ValidationError.
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
        raise NotImplementedError("TODO: Реализуйте change_status")

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
        raise NotImplementedError("TODO: Реализуйте to_dict")

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Создать задачу из словаря. Выбор класса по полю 'type'."""
        raise NotImplementedError("TODO: Реализуйте from_dict")

    # ── Displayable ─────────────────────────────────────────────────

    def short_display(self) -> str:
        """Краткое представление: [LABEL] title — PRIORITY — STATUS"""
        raise NotImplementedError("TODO: Реализуйте short_display")

    def full_display(self) -> str:
        """Полное представление со всеми полями."""
        raise NotImplementedError("TODO: Реализуйте full_display")

    # ── Магические методы (TODO: реализовать) ───────────────────────
    # __str__:  [BUG] #abc12 — Fix login (HIGH)
    # __repr__: Bug(id='abc12', title='Fix login', status=OPEN)
    # __eq__, __hash__: по id
    # __lt__, __le__, __gt__, __ge__: по priority.value
