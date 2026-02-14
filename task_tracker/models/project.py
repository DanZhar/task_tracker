"""Модель проекта."""

import uuid

from task_tracker.interfaces import Displayable, Serializable
from task_tracker.validators import StringLengthValidator


class Project(Serializable, Displayable):
    """Проект, содержащий задачи и участников (композиция).

    Поля:
        id (str): уникальный идентификатор (UUID4)
        name (str): название проекта (3–128 символов)
        tasks (list[Task]): список задач
        members (list[User]): участники проекта

    Магические методы (TODO: реализовать):
        __len__: количество задач
        __contains__: проверка наличия задачи по id (строка)
        __iter__: итерация по задачам
        __getitem__: получение задачи по индексу или срезу
        __str__: название проекта (N задач, M участников)
        __repr__: Project(id='...', name='...')
    """

    name = StringLengthValidator(min_length=3, max_length=128)

    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.tasks: list = []
        self.members: list = []

    # ── Serializable ────────────────────────────────────────────────

    def to_dict(self) -> dict:
        raise NotImplementedError("TODO: Реализуйте to_dict для Project")

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        raise NotImplementedError("TODO: Реализуйте from_dict для Project")

    # ── Displayable ─────────────────────────────────────────────────

    def short_display(self) -> str:
        raise NotImplementedError("TODO: Реализуйте short_display для Project")

    def full_display(self) -> str:
        raise NotImplementedError("TODO: Реализуйте full_display для Project")

    # ── Магические методы (TODO: реализовать) ───────────────────────
    # __len__: len(self.tasks)
    # __contains__: task_id (str) in project → True/False
    # __iter__: iter(self.tasks)
    # __getitem__: self.tasks[index] или self.tasks[slice]
