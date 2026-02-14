"""ABC-интерфейсы: Serializable, Displayable."""

from abc import ABC, abstractmethod


class Serializable(ABC):
    """Интерфейс сериализации в dict / из dict."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Сериализовать объект в словарь."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "Serializable":
        """Создать объект из словаря."""
        ...


class Displayable(ABC):
    """Интерфейс отображения."""

    @abstractmethod
    def short_display(self) -> str:
        """Краткое представление (для списков)."""
        ...

    @abstractmethod
    def full_display(self) -> str:
        """Полное представление (для детального просмотра)."""
        ...
