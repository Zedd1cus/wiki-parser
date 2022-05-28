"""
Модуль для тестирования Hash map
"""
from tests.map_tests import MapTesting
from src.maps.hash_map import HashMap


class HashMapTesting(MapTesting):
    """
    Класс для тестирования методов Hash map
    """
    h_test = HashMap

    def test_deletion(self) -> None:
        """
        Проверяет, действительно ли del удаляет элемент
        :return: None
        """
        self.map[1] = 'first'
        self.map[0] = 'will be deleted'
        del self.map[0]
        with self.assertRaises(KeyError):
            non_existing = self.map[0]
            non_existing += 1

    def test_inner_list_reduction(self) -> None:
        """
        Проверяет, уменьшается ли inner list хэш-таблицы,
        когда заполнено менее 30% list`a
        :return: None
        """
        self.map[1] = 'first'
        self.map[2] = 'second'
        self.map[3] = 'temp'
        old_capacity = self.map.get_capacity()
        del self.map[3]
        new_capacity = self.map.get_capacity()
        self.assertLess(new_capacity, old_capacity)

    def test_inner_list_expansion(self):
        """
        Проверяет, расширяется  ли inner list хэш-таблицы
        когда заполнено более 70% list`a
        :return: None
        """
        old_capacity = self.map.get_capacity()
        for i in range(self.map.get_capacity() - 1):
            self.map[i] = i*i
        new_capacity = self.map.get_capacity()
        self.assertLess(old_capacity, new_capacity)

    def test_same_size_when_rewritten(self):
        """
        Проверяет, не изменяется ли _size (количество элементов),
        когда значение элемента переписывается
        :return: None
        """
        self.map[1] = 'first'
        self.map[2] = 'second'
        old_size = len(self.map)
        self.map[2] = 'new second'
        new_size = len(self.map)
        self.assertEqual(old_size, new_size)

    def test_get(self):
        """
        Проверяет, правильно ли работает метод get.
        Возвращает значение, если ключ существует / по умолчанию, если ключ не существует
        :return: None
        """
        self.map[1] = 2
        check_has = self.map.get(1, 0)
        check_no = self.map.get(2, 0)
        self.assertEqual(check_has, 2)
        self.assertEqual(check_no, 0)
