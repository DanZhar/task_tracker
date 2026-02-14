"""Тесты дескрипторов валидации."""

import pytest

from task_tracker.exceptions import ValidationError
from task_tracker.validators import RangeValidator, StringLengthValidator

# ── Вспомогательные классы для тестирования дескрипторов ──────────


class RangeTestClass:
    value = RangeValidator(min_value=1, max_value=10)

    def __init__(self, v):
        self.value = v


class StringTestClass:
    name = StringLengthValidator(min_length=2, max_length=10)

    def __init__(self, n):
        self.name = n


# ── RangeValidator ───────────────────────────────────────────────


class TestRangeValidatorBasic:
    """Базовые тесты дескриптора RangeValidator."""

    def test_stores_valid_value(self):
        obj = RangeTestClass(5)
        assert obj.value == 5

    def test_stores_min_boundary(self):
        obj = RangeTestClass(1)
        assert obj.value == 1

    def test_stores_max_boundary(self):
        obj = RangeTestClass(10)
        assert obj.value == 10

    def test_update_value(self):
        obj = RangeTestClass(5)
        obj.value = 7
        assert obj.value == 7


class TestRangeValidatorRejectsInvalid:
    """RangeValidator должен отклонять невалидные значения."""

    def test_below_min_raises(self):
        with pytest.raises((ValueError, ValidationError)):
            RangeTestClass(0)

    def test_above_max_raises(self):
        with pytest.raises((ValueError, ValidationError)):
            RangeTestClass(11)

    def test_negative_raises(self):
        with pytest.raises((ValueError, ValidationError)):
            RangeTestClass(-5)

    def test_update_below_min_raises(self):
        obj = RangeTestClass(5)
        with pytest.raises((ValueError, ValidationError)):
            obj.value = 0

    def test_update_above_max_raises(self):
        obj = RangeTestClass(5)
        with pytest.raises((ValueError, ValidationError)):
            obj.value = 100

    def test_non_numeric_raises(self):
        with pytest.raises((TypeError, ValueError, ValidationError)):
            RangeTestClass("five")


class TestRangeValidatorDescriptorProtocol:
    """RangeValidator работает как дескриптор."""

    def test_class_access_returns_descriptor(self):
        assert isinstance(RangeTestClass.value, RangeValidator)

    def test_different_instances_independent(self):
        a = RangeTestClass(3)
        b = RangeTestClass(8)
        assert a.value == 3
        assert b.value == 8


# ── StringLengthValidator ────────────────────────────────────────


class TestStringLengthValidatorBasic:
    """Базовые тесты дескриптора StringLengthValidator."""

    def test_stores_valid_string(self):
        obj = StringTestClass("hello")
        assert obj.name == "hello"

    def test_stores_min_length(self):
        obj = StringTestClass("ab")
        assert obj.name == "ab"

    def test_stores_max_length(self):
        obj = StringTestClass("abcdefghij")  # 10 chars
        assert obj.name == "abcdefghij"

    def test_update_value(self):
        obj = StringTestClass("hello")
        obj.name = "world"
        assert obj.name == "world"


class TestStringLengthValidatorRejectsInvalid:
    """StringLengthValidator должен отклонять невалидные значения."""

    def test_too_short_raises(self):
        with pytest.raises((ValueError, ValidationError)):
            StringTestClass("a")

    def test_empty_raises(self):
        with pytest.raises((ValueError, ValidationError)):
            StringTestClass("")

    def test_too_long_raises(self):
        with pytest.raises((ValueError, ValidationError)):
            StringTestClass("x" * 11)

    def test_update_too_short_raises(self):
        obj = StringTestClass("hello")
        with pytest.raises((ValueError, ValidationError)):
            obj.name = "a"

    def test_non_string_raises(self):
        with pytest.raises((TypeError, ValueError, ValidationError)):
            StringTestClass(123)


class TestStringLengthDescriptorProtocol:
    """StringLengthValidator работает как дескриптор."""

    def test_class_access_returns_descriptor(self):
        assert isinstance(StringTestClass.name, StringLengthValidator)

    def test_different_instances_independent(self):
        a = StringTestClass("Alice")
        b = StringTestClass("Bob")
        assert a.name == "Alice"
        assert b.name == "Bob"
