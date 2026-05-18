"""Сохранение и загрузка данных в JSON.

Модуль работает с интерфейсом Serializable, а не с конкретными классами (DIP).
"""
import json
import os
from json import JSONDecodeError

from task_tracker.exceptions import StorageError
from task_tracker.models.project import Project


def save_data(projects: list, filepath: str) -> None:
    """Сохранить список проектов в JSON-файл.

    Формат файла:
    {
        "projects": [
            {
                "id": "uuid",
                "name": "My Project",
                "members": [...],
                "tasks": [...]
            }
        ]
    }

    Требования:
    - Каждый проект/задача/пользователь сериализуется через to_dict()
    - При ошибке записи — StorageError
    - JSON с отступами (indent=2) для читаемости

    Args:
        projects: список объектов Project
        filepath: путь к файлу
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filepath)

    try:
        projects_dicts = {"projects": [proj.to_dict() for proj in projects]}
    except TypeError as e:
        raise StorageError(f"Failed to serialize data: {e}") from e

    try:
        with open(filepath, 'w', encoding='utf-8') as dest_file:
            json.dump(projects_dicts, dest_file, indent=2)
    except OSError as e:
        raise StorageError(f"Failed to write JSON: {filepath}: {e}") from e


def load_data(filepath: str) -> list:
    """Загрузить список проектов из JSON-файла.

    Требования:
    - Если файл не существует — вернуть пустой список (не ошибка)
    - Для каждой задачи определить тип по полю "type" и вызвать from_dict()
    - При ошибке чтения/парсинга — StorageError

    Args:
        filepath: путь к файлу

    Returns:
        Список объектов Project
    """

    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filepath)

    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
    except JSONDecodeError as e:
        raise StorageError(f"Failed to parse JSON: {filepath}: {e}") from e
    except OSError as e:
        raise StorageError(f"Failed to open JSON: {filepath}: {e}") from e

    try:
        projects_data = data.get("projects", [])
        projects = [Project.from_dict(proj_data) for proj_data in projects_data]
        return projects
    except (ValueError, KeyError, TypeError) as e:
        raise StorageError(f"Failed to deserialize data: {filepath}: {e}") from e
