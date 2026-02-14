"""Дескрипторы валидации полей.

Дескрипторы используются для валидации данных при присвоении значений
атрибутам экземпляра. Работают на уровне класса через протокол дескрипторов
(__get__, __set__, __set_name__).

Пример использования:
    class Bug(Task):
        severity = RangeValidator(min_value=1, max_value=10)
"""

from task_tracker.exceptions import ValidationError  # noqa: F401


class RangeValidator:
    """Дескриптор: валидация числовых полей в заданном диапазоне [min_value, max_value].

    При попытке установить значение вне диапазона должен выбрасывать ValidationError.

    Требования:
    - Реализовать __set_name__, __get__, __set__
    - Хранить значение в атрибуте экземпляра с префиксом _ (например _severity)
    - При невалидном значении выбрасывать ValidationError с понятным сообщением
    - Проверять, что значение является числом (int или float)
    """

    def __init__(self, min_value: int | None = None, max_value: int | None = None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        # TODO: Добавьте валидацию:
        # 1. Проверьте, что value — число (int или float)
        # 2. Если min_value задан и value < min_value → ValidationError
        # 3. Если max_value задан и value > max_value → ValidationError
        setattr(obj, self.private_name, value)


class StringLengthValidator:
    """Дескриптор: валидация длины строковых полей [min_length, max_length].

    При попытке установить строку неподходящей длины должен выбрасывать ValidationError.

    Требования:
    - Реализовать __set_name__, __get__, __set__
    - Хранить значение в атрибуте экземпляра с префиксом _
    - При невалидном значении выбрасывать ValidationError
    - Проверять, что значение является строкой
    """

    def __init__(self, min_length: int = 0, max_length: int | None = None):
        self.min_length = min_length
        self.max_length = max_length

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        # TODO: Добавьте валидацию:
        # 1. Проверьте, что value — строка
        # 2. Если len(value) < min_length → ValidationError
        # 3. Если max_length задан и len(value) > max_length → ValidationError
        setattr(obj, self.private_name, value)
