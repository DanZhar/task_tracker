"""Точка входа приложения.

Запуск:
    python -m task_tracker.main [--data FILE]
    python -m task_tracker [--data FILE]
"""

import argparse


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Разобрать аргументы командной строки.

    Аргументы:
        --data FILE: путь к файлу данных (по умолчанию data.json)

    Args:
        args: список аргументов (None = sys.argv[1:])

    Returns:
        argparse.Namespace с полем data
    """
    raise NotImplementedError("TODO: Реализуйте parse_args")


def main() -> None:
    """Главная функция: парсинг аргументов → запуск CLI."""
    raise NotImplementedError("TODO: Реализуйте main")


if __name__ == "__main__":
    main()
