"""Миксины: TimestampMixin, HistoryMixin.

Миксины добавляют дополнительное поведение к классам через множественное наследование.
"""


class TimestampMixin:
    """Миксин: автоматическое обновление updated_at при изменении полей.

    Требования:
    - При любом изменении полей объекта обновлять self.updated_at = datetime.now()
    - Можно реализовать через переопределение __setattr__

    Подсказка:
        def __setattr__(self, name, value):
            super().__setattr__(name, value)
            if name != 'updated_at' and hasattr(self, 'updated_at'):
                super().__setattr__('updated_at', datetime.now())
    """

    # TODO: Реализуйте автообновление updated_at


class HistoryMixin:
    """Миксин: ведение истории изменений статуса.

    Атрибут:
        _history: list[dict] — список записей вида:
            {"from": "open", "to": "in_progress", "at": "2025-01-02T10:00:00"}

    Требования:
    - Инициализировать _history = [] (если отсутствует)
    - При каждом вызове change_status() добавлять запись в _history
    - Предоставить свойство history (read-only) для доступа к истории

    Подсказка: можно вызывать метод _record_transition(old, new) из change_status().
    """

    # TODO: Реализуйте ведение истории изменений статуса
