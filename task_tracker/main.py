"""Точка входа приложения.

Запуск:
    python -m task_tracker.main [--data FILE]
    python -m task_tracker [--data FILE]
"""

import argparse

from task_tracker.cli import run_cli


def valid_path(path_str: str) -> str:
    """Функция для валидации аргумента --data"""

    if not path_str.endswith(".json"):
        raise argparse.ArgumentError(f"{path_str} is not a JSON file")

    return path_str


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Разобрать аргументы командной строки.

    Аргументы:
        --data FILE: путь к файлу данных (по умолчанию data.json)

    Args:
        args: список аргументов (None = sys.argv[1:])

    Returns:
        argparse.Namespace с полем data
    """

    parser = argparse.ArgumentParser(
        prog="task_tracker", description="Console task tracker with context menu"
    )
    parser.add_argument(
        "--data", type=valid_path, default="data.json", help="Path to data storage file"
    )

    return parser.parse_args(args)


def main() -> None:
    """Главная функция: парсинг аргументов → запуск CLI."""

    args = parse_args()
    run_cli(args.data)


if __name__ == "__main__":
    main()
