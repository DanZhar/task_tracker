"""Тесты модели Project."""

import uuid

import pytest

from task_tracker.models.project import Project
from task_tracker.models.tasks import Bug


class TestProjectFields:
    """Тесты полей проекта."""

    def test_has_id(self, sample_project):
        assert isinstance(sample_project.id, str)
        uuid.UUID(sample_project.id)

    def test_name(self, sample_project):
        assert sample_project.name == "Test Project"

    def test_has_tasks_list(self, sample_project):
        assert isinstance(sample_project.tasks, list)

    def test_has_members_list(self, sample_project):
        assert isinstance(sample_project.members, list)

    def test_empty_project(self):
        p = Project(name="Empty")
        assert p.tasks == []
        assert p.members == []


class TestProjectNameValidation:
    """Валидация имени проекта (3–128 символов)."""

    def test_valid_name(self):
        p = Project(name="Abc")
        assert p.name == "Abc"

    def test_name_too_short_raises(self):
        with pytest.raises((ValueError, Exception)):
            Project(name="ab")

    def test_name_too_long_raises(self):
        with pytest.raises((ValueError, Exception)):
            Project(name="x" * 129)


class TestProjectLen:
    """__len__ возвращает количество задач."""

    def test_len_with_tasks(self, sample_project):
        assert len(sample_project) == 2

    def test_len_empty(self):
        p = Project(name="Empty")
        assert len(p) == 0

    def test_len_after_adding(self):
        p = Project(name="Test")
        p.tasks.append(Bug(title="Bug 1", severity=1))
        assert len(p) == 1
        p.tasks.append(Bug(title="Bug 2", severity=2))
        assert len(p) == 2


class TestProjectContains:
    """__contains__ — проверка наличия задачи по id."""

    def test_contains_existing_task(self, sample_project, sample_bug):
        assert sample_bug.id in sample_project

    def test_not_contains_absent(self, sample_project):
        assert "nonexistent-id" not in sample_project

    def test_contains_after_adding(self):
        p = Project(name="Test")
        bug = Bug(title="New bug", severity=1)
        p.tasks.append(bug)
        assert bug.id in p


class TestProjectIter:
    """__iter__ — итерация по задачам."""

    def test_iter_returns_tasks(self, sample_project):
        tasks = list(sample_project)
        assert len(tasks) == 2

    def test_iter_preserves_order(self, sample_project, sample_bug, sample_feature):
        tasks = list(sample_project)
        assert tasks[0].id == sample_bug.id
        assert tasks[1].id == sample_feature.id

    def test_iter_empty(self):
        p = Project(name="Empty")
        assert list(p) == []

    def test_for_loop(self, sample_project):
        count = 0
        for _ in sample_project:
            count += 1
        assert count == 2


class TestProjectGetItem:
    """__getitem__ — получение задачи по индексу или срезу."""

    def test_get_by_index(self, sample_project, sample_bug):
        assert sample_project[0].id == sample_bug.id

    def test_get_last(self, sample_project, sample_feature):
        assert sample_project[-1].id == sample_feature.id

    def test_get_slice(self, sample_project):
        sliced = sample_project[0:1]
        assert len(sliced) == 1

    def test_index_out_of_range(self, sample_project):
        with pytest.raises(IndexError):
            _ = sample_project[100]
