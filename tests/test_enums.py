"""Тесты перечислений и допустимых переходов статусов."""

from task_tracker.enums import VALID_TRANSITIONS, Priority, Role, Status


class TestStatus:
    """Тесты перечисления Status."""

    def test_open_value(self):
        assert Status.OPEN.value == "open"

    def test_in_progress_value(self):
        assert Status.IN_PROGRESS.value == "in_progress"

    def test_in_review_value(self):
        assert Status.IN_REVIEW.value == "in_review"

    def test_done_value(self):
        assert Status.DONE.value == "done"

    def test_closed_value(self):
        assert Status.CLOSED.value == "closed"

    def test_status_count(self):
        assert len(Status) == 5

    def test_from_string(self):
        assert Status("open") == Status.OPEN
        assert Status("in_progress") == Status.IN_PROGRESS


class TestPriority:
    """Тесты перечисления Priority."""

    def test_low_value(self):
        assert Priority.LOW.value == 1

    def test_medium_value(self):
        assert Priority.MEDIUM.value == 2

    def test_high_value(self):
        assert Priority.HIGH.value == 3

    def test_critical_value(self):
        assert Priority.CRITICAL.value == 4

    def test_priority_count(self):
        assert len(Priority) == 4

    def test_priorities_are_ordered_by_value(self):
        values = [p.value for p in Priority]
        assert values == sorted(values)


class TestRole:
    """Тесты перечисления Role."""

    def test_developer(self):
        assert Role.DEVELOPER.value == "developer"

    def test_qa(self):
        assert Role.QA.value == "qa"

    def test_team_lead(self):
        assert Role.TEAM_LEAD.value == "team_lead"

    def test_pm(self):
        assert Role.PM.value == "pm"

    def test_role_count(self):
        assert len(Role) == 4


class TestValidTransitions:
    """Тесты карты допустимых переходов статусов."""

    def test_all_statuses_have_transitions(self):
        for status in Status:
            assert status in VALID_TRANSITIONS

    def test_open_to_in_progress(self):
        assert Status.IN_PROGRESS in VALID_TRANSITIONS[Status.OPEN]

    def test_open_cannot_go_to_done(self):
        assert Status.DONE not in VALID_TRANSITIONS[Status.OPEN]

    def test_open_cannot_go_to_closed(self):
        assert Status.CLOSED not in VALID_TRANSITIONS[Status.OPEN]

    def test_in_progress_to_in_review(self):
        assert Status.IN_REVIEW in VALID_TRANSITIONS[Status.IN_PROGRESS]

    def test_in_progress_to_open(self):
        assert Status.OPEN in VALID_TRANSITIONS[Status.IN_PROGRESS]

    def test_in_review_to_done(self):
        assert Status.DONE in VALID_TRANSITIONS[Status.IN_REVIEW]

    def test_in_review_to_in_progress(self):
        assert Status.IN_PROGRESS in VALID_TRANSITIONS[Status.IN_REVIEW]

    def test_done_to_closed(self):
        assert Status.CLOSED in VALID_TRANSITIONS[Status.DONE]

    def test_done_to_in_progress(self):
        assert Status.IN_PROGRESS in VALID_TRANSITIONS[Status.DONE]

    def test_closed_is_terminal(self):
        assert len(VALID_TRANSITIONS[Status.CLOSED]) == 0
