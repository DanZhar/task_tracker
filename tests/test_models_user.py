"""Тесты модели User."""

import uuid

import pytest

from task_tracker.enums import Role
from task_tracker.models.user import User


class TestUserFields:
    """Тесты полей пользователя."""

    def test_has_id(self, alice):
        assert hasattr(alice, "id")
        assert isinstance(alice.id, str)

    def test_id_is_uuid(self, alice):
        uuid.UUID(alice.id)

    def test_unique_ids(self):
        u1 = User(name="User1")
        u2 = User(name="User2")
        assert u1.id != u2.id

    def test_name(self, alice):
        assert alice.name == "Alice"

    def test_role(self, alice):
        assert alice.role == Role.DEVELOPER

    def test_default_role(self):
        user = User(name="Default")
        assert user.role == Role.DEVELOPER


class TestUserNameValidation:
    """Валидация имени (2–64 символа)."""

    def test_valid_name(self):
        user = User(name="Al")
        assert user.name == "Al"

    def test_max_length_name(self):
        name = "x" * 64
        user = User(name=name)
        assert user.name == name

    def test_name_too_short_raises(self):
        with pytest.raises((ValueError, Exception)):
            User(name="A")

    def test_name_empty_raises(self):
        with pytest.raises((ValueError, Exception)):
            User(name="")

    def test_name_too_long_raises(self):
        with pytest.raises((ValueError, Exception)):
            User(name="x" * 65)


class TestUserRoles:
    """Тесты различных ролей."""

    def test_qa_role(self):
        user = User(name="Tester", role=Role.QA)
        assert user.role == Role.QA

    def test_team_lead_role(self):
        user = User(name="Lead", role=Role.TEAM_LEAD)
        assert user.role == Role.TEAM_LEAD

    def test_pm_role(self):
        user = User(name="Manager", role=Role.PM)
        assert user.role == Role.PM
