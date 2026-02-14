"""Сохранение и загрузка данных в JSON.

Модуль работает с интерфейсом Serializable, а не с конкретными классами (DIP).
"""


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
    raise NotImplementedError("TODO: Реализуйте save_data")


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
    raise NotImplementedError("TODO: Реализуйте load_data")
