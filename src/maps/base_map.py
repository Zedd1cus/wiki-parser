"""
Модуль для правильного создания map
"""
from abc import ABC, abstractmethod
from typing import Iterable, Tuple


class BaseMap(ABC):
    """
    Класс для карт с абстрактными методами и некоторым универсальным методом для всех maps
    """
    @abstractmethod
    def __getitem__(self, key: str) -> int:
        ...

    @abstractmethod
    def __setitem__(self, key: str, value: int) -> None:
        ...

    @abstractmethod
    def __delitem__(self, key: str) -> None:
        ...

    @abstractmethod
    def __iter__(self) -> Iterable[Tuple[str, int]]:
        ...

    def __contains__(self, key: str) -> bool:
        try:
            _ = self[key]
        except KeyError:
            return False
        return True

    def __eq__(self, other: 'BaseMap') -> bool:
        if len(self) != len(other):
            return False
        for key, value in self:
            try:
                if value != other[key]:
                    return False
            except KeyError:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __bool__(self) -> bool:
        return len(self) != 0

    def items(self) -> Iterable[Tuple[str, int]]:
        """Возвращает итерацию с кортежами k, v"""
        yield from self

    def values(self) -> Iterable[int]:
        """Возвращает итерацию, выполненную из значений карты"""
        return (value for key, value in self)

    def keys(self) -> Iterable[str]:
        """Rвозвращает итерацию, выполненную из ключей map"""
        return (key for key, value in self)

    @classmethod
    def fromkeys(cls, iterable, value=None) -> 'BaseMap':
        """Создает новую map с ключами из iterable и значениями"""
        res_map = cls()
        for key in iterable:
            res_map[key] = value
        return res_map

    def update(self, other=None) -> None:
        """Обновляет значения по ключам и значениям из other"""
        if other is None:
            return
        if hasattr(other, "keys"):
            for key in other.keys():
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value

    def get(self, key, default=None) -> int:
        """Возвращает значение по ключу, если ключ существует, в противном случае по умолчанию"""
        try:
            value = self[key]
        except KeyError:
            return default
        return value

    def pop(self, key, default=None):
        """
        Если ключ существует, функция удалит ключ и вернет его значение
        Иначе возвращает значение по умолчанию
        """
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError as key_err:
            if default is None:
                raise KeyError from key_err
            return default

    def popitem(self):
        """Удаляет и возвращает последнюю пару (ключ, значение) в виде 2-кортежа"""
        to_del_key = 0
        to_del_value = 0
        for key, value in self:
            to_del_key = key
            to_del_value = value
        del self[to_del_key]
        return to_del_key, to_del_value

    def setdefault(self, key, default=None):
        """
        Вставляет ключ со значением по умолчанию, если ключа нет на map.
        Возвращает значение для ключа, если ключ находится на map, в противном случае по умолчанию.
        """
        if key in self:
            return self[key]
        self[key] = default
        return default

    def sum(self):
        """Возвращает сумму значений"""
        return sum(value for key, value in self)

    @abstractmethod
    def clear(self):
        """Очищает map"""
        ...

    def write(self, path: str, mode='a') -> None:
        """Записывает map в файл"""
        with open(path, mode, encoding='utf8') as file:
            for key, value in self:
                file.write(f'{key} {value}\n')

    @classmethod
    def read(cls, path: str) -> 'BaseMap':
        """Считывает map из файла"""
        my_obj = cls()
        with open(path, 'r', encoding='utf8') as file:
            line = file.readline()
            while line != '':
                key, value = line.split()
                my_obj[key] = value
                line = file.readline()
        return my_obj
