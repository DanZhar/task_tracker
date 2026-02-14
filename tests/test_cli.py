"""Тесты CLI (парсинг аргументов)."""

from task_tracker.main import parse_args


class TestParseArgs:
    """Тесты разбора аргументов командной строки."""

    def test_default_data_file(self):
        args = parse_args([])
        assert args.data == "data.json"

    def test_custom_data_file(self):
        args = parse_args(["--data", "custom.json"])
        assert args.data == "custom.json"

    def test_data_is_string(self):
        args = parse_args(["--data", "myfile.json"])
        assert isinstance(args.data, str)
