"""Тесты конкретных типов задач: Bug, Feature, Epic."""

import pytest

from task_tracker.models.base import Task
from task_tracker.models.tasks import Bug, Epic, Feature

# ── Bug ──────────────────────────────────────────────────────────


class TestBugInheritance:
    def test_is_task(self, sample_bug):
        assert isinstance(sample_bug, Task)

    def test_is_bug(self, sample_bug):
        assert isinstance(sample_bug, Bug)


class TestBugFields:
    def test_severity(self, sample_bug):
        assert sample_bug.severity == 7

    def test_steps_to_reproduce(self, sample_bug):
        assert "Open app" in sample_bug.steps_to_reproduce

    def test_default_severity(self):
        bug = Bug(title="Default bug")
        assert bug.severity == 1

    def test_default_steps(self):
        bug = Bug(title="Default bug")
        assert bug.steps_to_reproduce == ""


class TestBugSeverityValidation:
    """severity валидируется через RangeValidator (1–10)."""

    def test_severity_min(self):
        bug = Bug(title="Min severity", severity=1)
        assert bug.severity == 1

    def test_severity_max(self):
        bug = Bug(title="Max severity", severity=10)
        assert bug.severity == 10

    def test_severity_below_min_raises(self):
        with pytest.raises((ValueError, Exception)):
            Bug(title="Bad severity", severity=0)

    def test_severity_above_max_raises(self):
        with pytest.raises((ValueError, Exception)):
            Bug(title="Bad severity", severity=11)


class TestBugEstimate:
    def test_estimate_formula(self):
        """estimate = severity * 2"""
        bug = Bug(title="Test", severity=7)
        assert bug.estimate() == 14.0

    def test_estimate_min_severity(self):
        bug = Bug(title="Test", severity=1)
        assert bug.estimate() == 2.0

    def test_estimate_max_severity(self):
        bug = Bug(title="Test", severity=10)
        assert bug.estimate() == 20.0

    def test_estimate_returns_float(self):
        bug = Bug(title="Test", severity=5)
        assert isinstance(bug.estimate(), (int, float))


class TestBugLabel:
    def test_label(self):
        bug = Bug(title="Test", severity=1)
        assert bug.label() == "[BUG]"


# ── Feature ──────────────────────────────────────────────────────


class TestFeatureInheritance:
    def test_is_task(self, sample_feature):
        assert isinstance(sample_feature, Task)

    def test_is_feature(self, sample_feature):
        assert isinstance(sample_feature, Feature)


class TestFeatureFields:
    def test_business_value(self, sample_feature):
        assert sample_feature.business_value == 8

    def test_complexity(self, sample_feature):
        assert sample_feature.complexity == 5

    def test_default_values(self):
        f = Feature(title="Default feature")
        assert f.business_value == 5
        assert f.complexity == 5


class TestFeatureValidation:
    """business_value и complexity валидируются через RangeValidator (1–10)."""

    def test_business_value_below_min(self):
        with pytest.raises((ValueError, Exception)):
            Feature(title="Bad", business_value=0)

    def test_business_value_above_max(self):
        with pytest.raises((ValueError, Exception)):
            Feature(title="Bad", business_value=11)

    def test_complexity_below_min(self):
        with pytest.raises((ValueError, Exception)):
            Feature(title="Bad", complexity=0)

    def test_complexity_above_max(self):
        with pytest.raises((ValueError, Exception)):
            Feature(title="Bad", complexity=11)


class TestFeatureEstimate:
    def test_estimate_formula(self):
        """estimate = (business_value + complexity) * 1.5"""
        f = Feature(title="Test", business_value=8, complexity=5)
        assert f.estimate() == (8 + 5) * 1.5

    def test_estimate_min_values(self):
        f = Feature(title="Test", business_value=1, complexity=1)
        assert f.estimate() == (1 + 1) * 1.5

    def test_estimate_max_values(self):
        f = Feature(title="Test", business_value=10, complexity=10)
        assert f.estimate() == (10 + 10) * 1.5

    def test_estimate_returns_float(self):
        f = Feature(title="Test", business_value=5, complexity=5)
        assert isinstance(f.estimate(), (int, float))


class TestFeatureLabel:
    def test_label(self):
        f = Feature(title="Test")
        assert f.label() == "[FEATURE]"


# ── Epic ─────────────────────────────────────────────────────────


class TestEpicInheritance:
    def test_is_task(self, sample_epic):
        assert isinstance(sample_epic, Task)

    def test_is_epic(self, sample_epic):
        assert isinstance(sample_epic, Epic)


class TestEpicFields:
    def test_has_subtasks(self, sample_epic):
        assert hasattr(sample_epic, "subtasks")
        assert isinstance(sample_epic.subtasks, list)

    def test_subtask_count(self, sample_epic):
        assert len(sample_epic.subtasks) == 2

    def test_default_empty_subtasks(self):
        epic = Epic(title="Empty epic")
        assert epic.subtasks == []


class TestEpicEstimate:
    def test_estimate_formula(self):
        """estimate = sum(subtask.estimate()) * 1.2"""
        bug = Bug(title="Bug", severity=5)  # estimate = 10
        feature = Feature(title="Feat", business_value=4, complexity=6)  # estimate = 15
        epic = Epic(title="Epic", subtasks=[bug, feature])
        # (10 + 15) * 1.2 = 30.0
        assert epic.estimate() == pytest.approx(30.0)

    def test_estimate_empty_subtasks(self):
        epic = Epic(title="Empty")
        assert epic.estimate() == 0.0

    def test_estimate_single_subtask(self):
        bug = Bug(title="Bug", severity=3)  # estimate = 6
        epic = Epic(title="Epic", subtasks=[bug])
        assert epic.estimate() == pytest.approx(6 * 1.2)


class TestEpicLabel:
    def test_label(self):
        epic = Epic(title="Test")
        assert epic.label() == "[EPIC]"
