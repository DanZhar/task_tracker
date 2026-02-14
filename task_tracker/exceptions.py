"""Пользовательские исключения проекта."""


class TaskTrackerError(Exception):
    """Базовое исключение проекта."""


class InvalidStatusTransitionError(TaskTrackerError):
    """Недопустимый переход между статусами задачи."""


class ValidationError(TaskTrackerError):
    """Ошибка валидации поля (длина, диапазон и т.д.)."""


class EntityNotFoundError(TaskTrackerError):
    """Задача, пользователь или проект не найден по ID."""


class StorageError(TaskTrackerError):
    """Ошибка чтения/записи файла данных."""


class DuplicateEntityError(TaskTrackerError):
    """Попытка добавить сущность-дубликат (например, пользователя с тем же именем)."""
