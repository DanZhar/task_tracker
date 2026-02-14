"""Тесты сохранения и загрузки данных (JSON)."""

import json

from task_tracker.enums import Priority, Role
from task_tracker.models.project import Project
from task_tracker.models.tasks import Bug, Feature
from task_tracker.models.user import User
from task_tracker.storage import load_data, save_data


class TestSaveData:
    """Тесты сохранения данных в JSON."""

    def test_save_creates_file(self, tmp_path, sample_project):
        filepath = str(tmp_path / "test.json")
        save_data([sample_project], filepath)
        assert (tmp_path / "test.json").exists()

    def test_save_produces_valid_json(self, tmp_path, sample_project):
        filepath = str(tmp_path / "test.json")
        save_data([sample_project], filepath)
        with open(filepath) as f:
            data = json.load(f)
        assert isinstance(data, dict)
        assert "projects" in data

    def test_save_project_structure(self, tmp_path, sample_project):
        filepath = str(tmp_path / "test.json")
        save_data([sample_project], filepath)
        with open(filepath) as f:
            data = json.load(f)
        project = data["projects"][0]
        assert "id" in project
        assert "name" in project
        assert "tasks" in project
        assert "members" in project

    def test_save_empty_list(self, tmp_path):
        filepath = str(tmp_path / "test.json")
        save_data([], filepath)
        with open(filepath) as f:
            data = json.load(f)
        assert data["projects"] == []


class TestLoadData:
    """Тесты загрузки данных из JSON."""

    def test_load_missing_file_returns_empty(self, tmp_path):
        filepath = str(tmp_path / "nonexistent.json")
        result = load_data(filepath)
        assert result == []

    def test_load_empty_projects(self, tmp_path):
        filepath = str(tmp_path / "empty.json")
        with open(filepath, "w") as f:
            json.dump({"projects": []}, f)
        result = load_data(filepath)
        assert result == []


class TestRoundTrip:
    """Тесты сериализации-десериализации (round-trip)."""

    def test_save_load_preserves_project_name(self, tmp_path, sample_project):
        filepath = str(tmp_path / "test.json")
        save_data([sample_project], filepath)
        loaded = load_data(filepath)
        assert len(loaded) == 1
        assert loaded[0].name == sample_project.name

    def test_save_load_preserves_tasks(self, tmp_path):
        project = Project(name="Test")
        bug = Bug(title="Bug one", severity=5, priority=Priority.HIGH)
        feature = Feature(title="Feature one", business_value=7, complexity=3)
        project.tasks.extend([bug, feature])

        filepath = str(tmp_path / "test.json")
        save_data([project], filepath)
        loaded = load_data(filepath)

        assert len(loaded[0].tasks) == 2

    def test_save_load_preserves_members(self, tmp_path):
        project = Project(name="Test")
        project.members.append(User(name="Alice", role=Role.DEVELOPER))

        filepath = str(tmp_path / "test.json")
        save_data([project], filepath)
        loaded = load_data(filepath)

        assert len(loaded[0].members) == 1
        assert loaded[0].members[0].name == "Alice"

    def test_save_load_preserves_task_type(self, tmp_path):
        project = Project(name="Test")
        project.tasks.append(Bug(title="A bug", severity=3))
        project.tasks.append(Feature(title="A feature", business_value=5, complexity=5))

        filepath = str(tmp_path / "test.json")
        save_data([project], filepath)
        loaded = load_data(filepath)

        assert isinstance(loaded[0].tasks[0], Bug)
        assert isinstance(loaded[0].tasks[1], Feature)

    def test_save_load_preserves_bug_severity(self, tmp_path):
        project = Project(name="Test")
        project.tasks.append(Bug(title="Bug", severity=8))

        filepath = str(tmp_path / "test.json")
        save_data([project], filepath)
        loaded = load_data(filepath)

        assert loaded[0].tasks[0].severity == 8

    def test_save_load_preserves_status(self, tmp_path):
        project = Project(name="Test")
        bug = Bug(title="Bug", severity=1)
        project.tasks.append(bug)

        filepath = str(tmp_path / "test.json")
        save_data([project], filepath)
        loaded = load_data(filepath)

        from task_tracker.enums import Status

        assert loaded[0].tasks[0].status == Status.OPEN
