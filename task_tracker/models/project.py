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

    Магические методы (реализовать):
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
        return {
            "id": self.id,
            "name": self.name,
            "tasks": [task.to_dict() for task in self.tasks],
            "members": [member.to_dict() for member in self.members],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        from task_tracker.models.base import Task
        from task_tracker.models.user import User

        obj = cls(name=data["name"])
        obj.id = data["id"]

        obj.members = [User.from_dict(member_data) for member_data in data.get("members", [])]
        obj.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]

        members_by_id = {member.id: member for member in obj.members}
        for task in obj.tasks:
            assignee_id = getattr(task, "_assignee_id", None)
            if assignee_id:
                task.assignee = members_by_id.get(assignee_id)

        return obj

    # ── Displayable ─────────────────────────────────────────────────

    def short_display(self) -> str:
        return str(self)

    def full_display(self) -> str:
        lines = [f"Project : {self.name}", f"ID      : {self.id}", f"Members : {len(self.members)}"]

        for i, member in enumerate(self.members, start=1):
            lines.append(f"    {i}. {member.short_display()}")

        lines.append(f"Tasks   : {len(self.tasks)}")
        for i, task in enumerate(self.tasks, start=1):
            lines.append(f"    {i}. {task.short_display()}")

        return "\n".join(lines)

    # ── Магические методы (TODO: реализовать) ───────────────────────
    def __len__(self) -> int:
        return len(self.tasks)

    def __contains__(self, task_id: str) -> bool:
        return task_id in (task.id for task in self.tasks)

    def __iter__(self):
        return iter(self.tasks)

    def __getitem__(self, index):
        return self.tasks[index]

    def __str__(self):
        return f"{self.name} ({len(self.tasks)} задач, {len(self.members)} участников)"

    def __repr__(self):
        return f"Project(id={self.id}, name={self.name!r})"
