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
        raise NotImplementedError("TODO: Реализуйте estimate для Bug")

    def label(self) -> str:
        """Метка: [BUG]"""
        raise NotImplementedError("TODO: Реализуйте label для Bug")


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
        raise NotImplementedError("TODO: Реализуйте estimate для Feature")

    def label(self) -> str:
        """Метка: [FEATURE]"""
        raise NotImplementedError("TODO: Реализуйте label для Feature")


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
        raise NotImplementedError("TODO: Реализуйте estimate для Epic")

    def label(self) -> str:
        """Метка: [EPIC]"""
        raise NotImplementedError("TODO: Реализуйте label для Epic")
