"""Конкретные типы задач: Bug, Feature, Epic."""

from task_tracker.enums import Priority
from task_tracker.models.base import Task
from task_tracker.validators import RangeValidator


class Bug(Task):
    """Баг-репорт.

    Дополнительные поля:
        severity (int): критичность от 1 до 10 (через RangeValidator)
        steps_to_reproduce (str): шаги воспроизведения

    Оценка трудоёмкости: severity * 2 часов
    Метка: [BUG]
    """

    severity = RangeValidator(min_value=1, max_value=10)

    def __init__(
            self,
            title: str,
            description: str = "",
            priority: Priority = Priority.MEDIUM,
            severity: int = 1,
            steps_to_reproduce: str = "",
    ):
        super().__init__(title, description, priority)
        self.severity = severity
        self.steps_to_reproduce = steps_to_reproduce

    def estimate(self) -> float:
        """Оценка: severity * 2 часов."""

        return self.severity * 2

    def label(self) -> str:
        """Метка: [BUG]"""

        return "[BUG]"

    def to_dict(self) -> dict:
        base_d = super().to_dict()

        base_d["severity"] = self.severity
        base_d["steps_to_reproduce"] = self.steps_to_reproduce

        return base_d

    @classmethod
    def from_dict(cls, data: dict) -> "Bug":
        obj = cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority(data["priority"]),
            severity=data.get("severity", 1),
            steps_to_reproduce=data.get("steps_to_reproduce", "")
        )

        obj._restore_fields(data)
        return obj

    def _display_lines(self) -> list[str]:
        lines = super()._display_lines()
        lines.append(f"  Severity : {self.severity}/10")
        if self.steps_to_reproduce:
            lines.append(f"  Steps    : {self.steps_to_reproduce}")
        return lines


class Feature(Task):
    """Запрос на новую функциональность.

    Дополнительные поля:
        business_value (int): бизнес-ценность от 1 до 10 (через RangeValidator)
        complexity (int): техническая сложность от 1 до 10 (через RangeValidator)

    Оценка трудоёмкости: (business_value + complexity) * 1.5 часов
    Метка: [FEATURE]
    """

    business_value = RangeValidator(min_value=1, max_value=10)
    complexity = RangeValidator(min_value=1, max_value=10)

    def __init__(
            self,
            title: str,
            description: str = "",
            priority: Priority = Priority.MEDIUM,
            business_value: int = 5,
            complexity: int = 5,
    ):
        super().__init__(title, description, priority)
        self.business_value = business_value
        self.complexity = complexity

    def estimate(self) -> float:
        """Оценка: (business_value + complexity) * 1.5 часов."""

        return (self.business_value + self.complexity) * 1.5

    def label(self) -> str:
        """Метка: [FEATURE]"""
        return "[FEATURE]"

    def to_dict(self) -> dict:
        base_d = super().to_dict()

        base_d["business_value"] = self.business_value
        base_d["complexity"] = self.complexity

        return base_d

    @classmethod
    def from_dict(cls, data: dict) -> "Feature":
        obj = cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority(data["priority"]),
            business_value=data.get("business_value", 5),
            complexity=data.get("complexity", 5)
        )

        obj._restore_fields(data)
        return obj

    def _display_lines(self) -> list[str]:
        lines = super()._display_lines()
        lines.append(f"  Biz value: {self.business_value}/10")
        lines.append(f"  Complexity: {self.complexity}/10")
        return lines


class Epic(Task):
    """Эпик — крупная задача, содержащая подзадачи.

    Дополнительные поля:
        subtasks (list[Task]): список подзадач (Bug или Feature)

    Оценка трудоёмкости: сумма estimate() всех подзадач × 1.2
    Метка: [EPIC]
    """

    def __init__(
            self,
            title: str,
            description: str = "",
            priority: Priority = Priority.MEDIUM,
            subtasks: list | None = None,
    ):
        super().__init__(title, description, priority)
        self.subtasks: list[Task] = subtasks if subtasks is not None else []

    def estimate(self) -> float:
        """Оценка: сумма estimate() подзадач × 1.2 (коэффициент координации)."""
        return sum(task.estimate() for task in self.subtasks) * 1.2

    def label(self) -> str:
        """Метка: [EPIC]"""
        return "[EPIC]"

    def to_dict(self) -> dict:
        base_d = super().to_dict()
        base_d["subtasks"] = [t.to_dict() for t in self.subtasks]
        return base_d

    @classmethod
    def from_dict(cls, data: dict) -> "Epic":
        obj = cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority(data["priority"]),
            subtasks=data.get("subtasks", None),
        )

        obj._restore_fields(data)
        return obj

    def _display_lines(self) -> list[str]:
        lines = super()._display_lines()
        lines.append(f"  Subtasks : {len(self.subtasks)}")
        for sub in self.subtasks:
            lines.append(f"    — {sub.short_display()}")
        return lines
