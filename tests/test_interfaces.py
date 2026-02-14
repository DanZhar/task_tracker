"""Тесты ABC-интерфейсов: Serializable, Displayable."""

from abc import ABC

import pytest

from task_tracker.interfaces import Displayable, Serializable


class TestSerializableInterface:
    """Serializable — ABC с to_dict и from_dict."""

    def test_is_abc(self):
        assert issubclass(Serializable, ABC)

    def test_has_to_dict(self):
        assert hasattr(Serializable, "to_dict")

    def test_has_from_dict(self):
        assert hasattr(Serializable, "from_dict")

    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            Serializable()


class TestDisplayableInterface:
    """Displayable — ABC с short_display и full_display."""

    def test_is_abc(self):
        assert issubclass(Displayable, ABC)

    def test_has_short_display(self):
        assert hasattr(Displayable, "short_display")

    def test_has_full_display(self):
        assert hasattr(Displayable, "full_display")

    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            Displayable()


class TestModelsImplementInterfaces:
    """Все модели реализуют нужные интерфейсы."""

    def test_bug_is_serializable(self, sample_bug):
        assert isinstance(sample_bug, Serializable)

    def test_bug_is_displayable(self, sample_bug):
        assert isinstance(sample_bug, Displayable)

    def test_feature_is_serializable(self, sample_feature):
        assert isinstance(sample_feature, Serializable)

    def test_feature_is_displayable(self, sample_feature):
        assert isinstance(sample_feature, Displayable)

    def test_epic_is_serializable(self, sample_epic):
        assert isinstance(sample_epic, Serializable)

    def test_user_is_serializable(self, alice):
        assert isinstance(alice, Serializable)

    def test_user_is_displayable(self, alice):
        assert isinstance(alice, Displayable)

    def test_project_is_serializable(self, sample_project):
        assert isinstance(sample_project, Serializable)

    def test_project_is_displayable(self, sample_project):
        assert isinstance(sample_project, Displayable)
