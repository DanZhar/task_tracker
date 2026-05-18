"""Миксины: TimestampMixin, HistoryMixin.

Миксины добавляют дополнительное поведение к классам через множественное наследование.
"""

from datetime import datetime


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

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name != "updated_at" and hasattr(self, "updated_at"):
            super().__setattr__("updated_at", datetime.now())


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

    def _ensure_history(self):
        if not hasattr(self, "_history"):
            self._history = []

    @property
    def history(self):
        self._ensure_history()
        return self._history

    def _record_transition(self, old_status, new_status) -> None:
        self._ensure_history()

        transition = {
            "from": old_status.value,
            "to": new_status.value,
            "at": datetime.now().isoformat(),
        }
        self._history.append(transition)
