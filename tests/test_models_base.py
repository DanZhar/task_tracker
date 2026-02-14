"""Тесты абстрактного базового класса Task."""

import uuid

import pytest

from task_tracker.enums import Priority, Status
from task_tracker.exceptions import InvalidStatusTransitionError
from task_tracker.models.base import Task
from task_tracker.models.tasks import Bug


class TestTaskIsAbstract:
    """Task — абстрактный класс, его нельзя инстанцировать напрямую."""

    def test_cannot_instantiate_task(self):
        with pytest.raises(TypeError):
            Task(title="test")


class TestTaskFields:
    """Тесты полей задачи."""

    def test_has_id(self, sample_bug):
        assert hasattr(sample_bug, "id")
        assert isinstance(sample_bug.id, str)

    def test_id_is_valid_uuid(self, sample_bug):
        uuid.UUID(sample_bug.id)  # не должно бросить исключение

    def test_unique_ids(self):
        bug1 = Bug(title="Bug 1", severity=1)
        bug2 = Bug(title="Bug 2", severity=1)
        assert bug1.id != bug2.id

    def test_has_title(self, sample_bug):
        assert sample_bug.title == "Fix login"

    def test_has_description(self, sample_bug):
        assert sample_bug.description == "Login page crashes on submit"

    def test_has_priority(self, sample_bug):
        assert sample_bug.priority == Priority.HIGH

    def test_has_created_at(self, sample_bug):
        assert sample_bug.created_at is not None

    def test_has_updated_at(self, sample_bug):
        assert sample_bug.updated_at is not None

    def test_assignee_default_none(self, sample_bug):
        assert sample_bug.assignee is None

    def test_initial_status_is_open(self, sample_bug):
        assert sample_bug.status == Status.OPEN


class TestTaskTitleValidation:
    """Валидация title через property (3–128 символов)."""

    def test_valid_title(self):
        bug = Bug(title="Fix", severity=1)
        assert bug.title == "Fix"

    def test_title_min_length(self):
        bug = Bug(title="abc", severity=1)
        assert bug.title == "abc"

    def test_title_max_length(self):
        title = "x" * 128
        bug = Bug(title=title, severity=1)
        assert bug.title == title

    def test_title_too_short_raises(self):
        with pytest.raises((ValueError, Exception)):
            Bug(title="ab", severity=1)

    def test_title_empty_raises(self):
        with pytest.raises((ValueError, Exception)):
            Bug(title="", severity=1)

    def test_title_too_long_raises(self):
        with pytest.raises((ValueError, Exception)):
            Bug(title="x" * 129, severity=1)

    def test_update_title_valid(self, sample_bug):
        sample_bug.title = "New title"
        assert sample_bug.title == "New title"

    def test_update_title_too_short_raises(self, sample_bug):
        with pytest.raises((ValueError, Exception)):
            sample_bug.title = "ab"


class TestTaskStatusTransitions:
    """Переходы между статусами через change_status()."""

    def test_open_to_in_progress(self, sample_bug):
        sample_bug.change_status(Status.IN_PROGRESS)
        assert sample_bug.status == Status.IN_PROGRESS

    def test_in_progress_to_in_review(self, sample_bug):
        sample_bug.change_status(Status.IN_PROGRESS)
        sample_bug.change_status(Status.IN_REVIEW)
        assert sample_bug.status == Status.IN_REVIEW

    def test_in_review_to_done(self, sample_bug):
        sample_bug.change_status(Status.IN_PROGRESS)
        sample_bug.change_status(Status.IN_REVIEW)
        sample_bug.change_status(Status.DONE)
        assert sample_bug.status == Status.DONE

    def test_done_to_closed(self, sample_bug):
        sample_bug.change_status(Status.IN_PROGRESS)
        sample_bug.change_status(Status.IN_REVIEW)
        sample_bug.change_status(Status.DONE)
        sample_bug.change_status(Status.CLOSED)
        assert sample_bug.status == Status.CLOSED

    def test_open_to_done_raises(self, sample_bug):
        with pytest.raises(InvalidStatusTransitionError):
            sample_bug.change_status(Status.DONE)

    def test_open_to_closed_raises(self, sample_bug):
        with pytest.raises(InvalidStatusTransitionError):
            sample_bug.change_status(Status.CLOSED)

    def test_closed_is_terminal(self, sample_bug):
        sample_bug.change_status(Status.IN_PROGRESS)
        sample_bug.change_status(Status.IN_REVIEW)
        sample_bug.change_status(Status.DONE)
        sample_bug.change_status(Status.CLOSED)
        with pytest.raises(InvalidStatusTransitionError):
            sample_bug.change_status(Status.OPEN)

    def test_in_progress_back_to_open(self, sample_bug):
        sample_bug.change_status(Status.IN_PROGRESS)
        sample_bug.change_status(Status.OPEN)
        assert sample_bug.status == Status.OPEN

    def test_cannot_set_status_directly(self, sample_bug):
        """status — read-only property, изменение через _status не рекомендуется."""
        # Тест проверяет, что есть property, блокирующее прямую запись
        with pytest.raises(AttributeError):
            sample_bug.status = Status.DONE


class TestTaskMagicStr:
    """Магические методы __str__ и __repr__."""

    def test_str_contains_label(self, sample_bug):
        s = str(sample_bug)
        assert "[BUG]" in s

    def test_str_contains_title(self, sample_bug):
        s = str(sample_bug)
        assert "Fix login" in s

    def test_str_contains_priority(self, sample_bug):
        s = str(sample_bug)
        assert "HIGH" in s

    def test_repr_contains_class_name(self, sample_bug):
        r = repr(sample_bug)
        assert "Bug" in r

    def test_repr_contains_title(self, sample_bug):
        r = repr(sample_bug)
        assert "Fix login" in r

    def test_repr_contains_status(self, sample_bug):
        r = repr(sample_bug)
        assert "OPEN" in r


class TestTaskEquality:
    """__eq__ и __hash__ — сравнение по id."""

    def test_same_object_equal(self, sample_bug):
        assert sample_bug == sample_bug

    def test_different_objects_not_equal(self):
        bug1 = Bug(title="Bug 1", severity=1)
        bug2 = Bug(title="Bug 2", severity=1)
        assert bug1 != bug2

    def test_equal_by_id(self):
        bug1 = Bug(title="Bug 1", severity=1)
        bug2 = Bug(title="Bug 2", severity=2)
        bug2.id = bug1.id
        assert bug1 == bug2

    def test_hashable(self, sample_bug):
        s = {sample_bug}
        assert sample_bug in s

    def test_same_hash_for_same_id(self):
        bug1 = Bug(title="Bug 1", severity=1)
        bug2 = Bug(title="Bug 2", severity=2)
        bug2.id = bug1.id
        assert hash(bug1) == hash(bug2)

    def test_can_use_in_dict(self, sample_bug):
        d = {sample_bug: "value"}
        assert d[sample_bug] == "value"


class TestTaskComparison:
    """__lt__, __le__, __gt__, __ge__ — сравнение по priority."""

    def test_low_less_than_high(self):
        low = Bug(title="Low bug", severity=1, priority=Priority.LOW)
        high = Bug(title="High bug", severity=1, priority=Priority.HIGH)
        assert low < high

    def test_high_greater_than_low(self):
        low = Bug(title="Low bug", severity=1, priority=Priority.LOW)
        high = Bug(title="High bug", severity=1, priority=Priority.HIGH)
        assert high > low

    def test_same_priority_not_less(self):
        bug1 = Bug(title="Bug 1", severity=1, priority=Priority.MEDIUM)
        bug2 = Bug(title="Bug 2", severity=1, priority=Priority.MEDIUM)
        assert not (bug1 < bug2)

    def test_le_same_priority(self):
        bug1 = Bug(title="Bug 1", severity=1, priority=Priority.MEDIUM)
        bug2 = Bug(title="Bug 2", severity=1, priority=Priority.MEDIUM)
        assert bug1 <= bug2

    def test_ge_same_priority(self):
        bug1 = Bug(title="Bug 1", severity=1, priority=Priority.MEDIUM)
        bug2 = Bug(title="Bug 2", severity=1, priority=Priority.MEDIUM)
        assert bug1 >= bug2

    def test_sortable(self):
        critical = Bug(title="C", severity=1, priority=Priority.CRITICAL)
        low = Bug(title="L", severity=1, priority=Priority.LOW)
        high = Bug(title="H", severity=1, priority=Priority.HIGH)
        medium = Bug(title="M", severity=1, priority=Priority.MEDIUM)

        sorted_tasks = sorted([critical, low, high, medium])
        priorities = [t.priority for t in sorted_tasks]
        assert priorities == [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL]


class TestTaskAssignee:
    """Назначение исполнителя."""

    def test_assign_user(self, sample_bug, alice):
        sample_bug.assignee = alice
        assert sample_bug.assignee == alice

    def test_unassign(self, sample_bug, alice):
        sample_bug.assignee = alice
        sample_bug.assignee = None
        assert sample_bug.assignee is None
