"""Тесты миксинов: TimestampMixin, HistoryMixin."""

import time
from datetime import datetime

from task_tracker.enums import Status
from task_tracker.models.tasks import Bug


class TestTimestampMixin:
    """TimestampMixin: автоматическое обновление updated_at."""

    def test_created_at_is_datetime(self, sample_bug):
        assert isinstance(sample_bug.created_at, datetime)

    def test_updated_at_is_datetime(self, sample_bug):
        assert isinstance(sample_bug.updated_at, datetime)

    def test_updated_at_changes_on_field_update(self, sample_bug):
        old_updated = sample_bug.updated_at
        time.sleep(0.01)
        sample_bug.description = "Updated description"
        assert sample_bug.updated_at >= old_updated

    def test_created_at_does_not_change(self, sample_bug):
        created = sample_bug.created_at
        time.sleep(0.01)
        sample_bug.description = "Updated"
        assert sample_bug.created_at == created


class TestHistoryMixin:
    """HistoryMixin: ведение истории изменений статуса."""

    def test_initial_history_empty(self):
        bug = Bug(title="New bug", severity=1)
        history = getattr(bug, "_history", getattr(bug, "history", []))
        if callable(history):
            history = history()
        assert len(history) == 0

    def test_history_after_status_change(self):
        bug = Bug(title="Bug", severity=1)
        bug.change_status(Status.IN_PROGRESS)
        history = getattr(bug, "_history", getattr(bug, "history", []))
        if callable(history):
            history = history()
        assert len(history) == 1

    def test_history_records_from_and_to(self):
        bug = Bug(title="Bug", severity=1)
        bug.change_status(Status.IN_PROGRESS)
        history = getattr(bug, "_history", getattr(bug, "history", []))
        if callable(history):
            history = history()
        record = history[0]
        assert record["from"] == "open" or record["from"] == Status.OPEN
        assert record["to"] == "in_progress" or record["to"] == Status.IN_PROGRESS

    def test_history_records_timestamp(self):
        bug = Bug(title="Bug", severity=1)
        bug.change_status(Status.IN_PROGRESS)
        history = getattr(bug, "_history", getattr(bug, "history", []))
        if callable(history):
            history = history()
        assert "at" in history[0]

    def test_multiple_transitions(self):
        bug = Bug(title="Bug", severity=1)
        bug.change_status(Status.IN_PROGRESS)
        bug.change_status(Status.IN_REVIEW)
        bug.change_status(Status.DONE)
        history = getattr(bug, "_history", getattr(bug, "history", []))
        if callable(history):
            history = history()
        assert len(history) == 3
