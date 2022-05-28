"""
Модуль для тестирования map
"""
from test import mapping_tests
from abc import ABC


class MapTesting(ABC, mapping_tests.BasicTestMappingProtocol):
    """
    Абстрактный класс с базовыми тестами для map
    """
    h_test = ABC

    def setUp(self):
        """
        Создает экземпляр класса map
        :return: None
        """
        self.map = self.h_test()

    def test_set_get_item(self):
        """
        Методы набора/получения элементов тестов
        :return: None
        """
        # тест для установки первого значения ключа
        self.map[1] = 'first'
        self.assertEqual(self.map[1], 'first')
        # тест для установки второго значения ключа
        self.map[10] = 'second'
        self.assertEqual(self.map[10], 'second')
        # тест на перезапись значения существующего ключа
        self.map[1] = 'rewritten'
        self.assertEqual(self.map[1], 'rewritten')

    def test_raise_key_error(self):
        """
        Проверяет, не возникает ли ошибка, когда ключ не существует
        :return: None
        """
        with self.assertRaises(KeyError):
            non_existing = self.map[0]
            non_existing += 1

    def test_rewrite_value(self):
        """
        Проверяет, переписано ли значение элемента с существующим ключом
        и не создается ли новый элемент
        :return: None
        """
        self.map[1] = 'old value'
        self.map[1] = 'new value'
        self.assertEqual(self.map[1], 'new value')

    def test_read_data(self):
        """
        Проверяет, правильно ли функция считывает данные из файла
        :return: None
        """
        filepath = 'files/to_read.txt'
        self.map = self.map.read(filepath)
        self.assertEqual(len(self.map), 3)
        self.assertEqual(self.map['babagi'], 'fortaite')

    def test_write_data(self):
        """
        Проверяет, правильно ли функция записывает данные в файл
        :return: None
        """
        filepath = 'files/to_write.txt'
        self.map[1] = 'first'
        self.map[2] = 'second'
        self.map.write(filepath, 'w')
        with open(filepath, 'r', encoding='utf8') as file:
            line = file.readline()
            while line:
                key, value = line.split()
                key = int(key)
                self.assertEqual(value, self.map[key])
                line = file.readline()
