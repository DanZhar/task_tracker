# Консольный Task Tracker

[![Run Tests](../../actions/workflows/run-tests.yml/badge.svg)](../../actions/workflows/run-tests.yml)

## Описание

Практический проект: консольный трекер задач с интерактивным меню на Python 3.10+.

Проект направлен на практику **ООП**: наследование, полиморфизм, инкапсуляция, композиция, ABC, дескрипторы, миксины, магические методы, SOLID.

## Как работать с проектом (для учеников)

### 1. Форкните репозиторий

Нажмите кнопку **Fork** в правом верхнем углу.

### 2. Клонируйте и настройте окружение

```bash
git clone https://github.com/<ваш-username>/task_tracker.git
cd task_tracker
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install pytest ruff
```

### 3. Реализуйте функции

Все файлы в `task_tracker/` содержат заглушки. Ваша задача — написать реализацию.

### 4. Проверяйте локально

```bash
pytest -v
ruff check .
ruff format --check .
```

### 5. Создайте Pull Request

Запушьте изменения и создайте PR в основной репозиторий. CI запустит проверки автоматически.

## Запуск

```bash
python -m task_tracker.main [--data FILE]
```

| Параметр      | По умолчанию | Описание                           |
| ------------- | ------------ | ---------------------------------- |
| `--data FILE` | `data.json`  | Путь к файлу для хранения данных   |

## Структура проекта

```
task_tracker/
├── pyproject.toml
├── README.md
├── task_tracker/
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py              # точка входа
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py           # абстрактный базовый класс Task
│   │   ├── tasks.py           # Bug, Feature, Epic
│   │   ├── user.py            # User
│   │   └── project.py         # Project
│   ├── enums.py               # Status, Priority, Role
│   ├── validators.py          # дескрипторы валидации
│   ├── mixins.py              # TimestampMixin, HistoryMixin
│   ├── interfaces.py          # Serializable, Displayable
│   ├── storage.py             # JSON-хранилище
│   ├── exceptions.py          # пользовательские исключения
│   └── cli.py                 # интерактивное меню
└── tests/
    ├── conftest.py
    ├── test_enums.py
    ├── test_exceptions.py
    ├── test_validators.py
    ├── test_models_base.py
    ├── test_models_tasks.py
    ├── test_models_user.py
    ├── test_models_project.py
    ├── test_mixins.py
    ├── test_interfaces.py
    ├── test_storage.py
    └── test_cli.py
```

## Ключевые требования

- **Наследование**: `Task` (ABC) → `Bug`, `Feature`, `Epic`
- **Полиморфизм**: `estimate()`, `label()` — разное поведение для каждого типа
- **Инкапсуляция**: `_status` через `change_status()`, `title` через property
- **Дескрипторы**: `RangeValidator`, `StringLengthValidator` для валидации полей
- **Миксины**: `TimestampMixin`, `HistoryMixin`
- **Магические методы**: `__str__`, `__repr__`, `__eq__`, `__lt__`, `__len__`, `__contains__`, `__iter__`, `__getitem__`
- **Сериализация**: JSON через интерфейс `Serializable`
- **Ограничения**: только стандартная библиотека Python

## CI/CD

На каждый PR автоматически запускаются:

1. **Lint & Format** — ruff
2. **Tests** — pytest на Python 3.10, 3.11, 3.12
3. **Structure Check** — наличие файлов + проверка запрещённых импортов
