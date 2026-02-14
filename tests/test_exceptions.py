"""Тесты пользовательских исключений."""

import pytest

from task_tracker.exceptions import (
    DuplicateEntityError,
    EntityNotFoundError,
    InvalidStatusTransitionError,
    StorageError,
    TaskTrackerError,
    ValidationError,
)


class TestExceptionHierarchy:
    """Все исключения наследуются от TaskTrackerError."""

    def test_base_is_exception(self):
        assert issubclass(TaskTrackerError, Exception)

    def test_invalid_status_transition(self):
        assert issubclass(InvalidStatusTransitionError, TaskTrackerError)

    def test_validation_error(self):
        assert issubclass(ValidationError, TaskTrackerError)

    def test_entity_not_found(self):
        assert issubclass(EntityNotFoundError, TaskTrackerError)

    def test_storage_error(self):
        assert issubclass(StorageError, TaskTrackerError)

    def test_duplicate_entity(self):
        assert issubclass(DuplicateEntityError, TaskTrackerError)


class TestExceptionUsage:
    """Исключения можно создавать, бросать и ловить."""

    def test_raise_and_catch_base(self):
        with pytest.raises(TaskTrackerError):
            raise TaskTrackerError("base error")

    def test_raise_invalid_status(self):
        with pytest.raises(TaskTrackerError):
            raise InvalidStatusTransitionError("OPEN -> DONE is not allowed")

    def test_raise_validation(self):
        with pytest.raises(TaskTrackerError):
            raise ValidationError("Title too short")

    def test_raise_entity_not_found(self):
        with pytest.raises(TaskTrackerError):
            raise EntityNotFoundError("Task abc123 not found")

    def test_raise_storage(self):
        with pytest.raises(TaskTrackerError):
            raise StorageError("Cannot write file")

    def test_raise_duplicate(self):
        with pytest.raises(TaskTrackerError):
            raise DuplicateEntityError("User Alice already exists")

    def test_message_preserved(self):
        msg = "specific error message"
        try:
            raise ValidationError(msg)
        except ValidationError as e:
            assert str(e) == msg
