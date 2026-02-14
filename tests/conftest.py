"""Фикстуры для тестов."""

import pytest

from task_tracker.enums import Priority, Role
from task_tracker.models.project import Project
from task_tracker.models.tasks import Bug, Epic, Feature
from task_tracker.models.user import User


@pytest.fixture
def alice():
    """Пользователь-разработчик."""
    return User(name="Alice", role=Role.DEVELOPER)


@pytest.fixture
def bob():
    """Пользователь-тестировщик."""
    return User(name="Bob", role=Role.QA)


@pytest.fixture
def sample_bug():
    """Баг с severity=7."""
    return Bug(
        title="Fix login",
        description="Login page crashes on submit",
        priority=Priority.HIGH,
        severity=7,
        steps_to_reproduce="1. Open app\n2. Click login\n3. Observe crash",
    )


@pytest.fixture
def sample_feature():
    """Фича с business_value=8, complexity=5."""
    return Feature(
        title="Add search",
        description="Implement full-text search",
        priority=Priority.MEDIUM,
        business_value=8,
        complexity=5,
    )


@pytest.fixture
def sample_epic(sample_bug, sample_feature):
    """Эпик с двумя подзадачами."""
    return Epic(
        title="User module",
        description="Complete user management module",
        priority=Priority.HIGH,
        subtasks=[sample_bug, sample_feature],
    )


@pytest.fixture
def sample_project(alice, bob, sample_bug, sample_feature):
    """Проект с участниками и задачами."""
    project = Project(name="Test Project")
    project.members.extend([alice, bob])
    project.tasks.extend([sample_bug, sample_feature])
    return project
