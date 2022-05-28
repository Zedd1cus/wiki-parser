"""
Модуль для тестирования Binary Tree Map
"""
from tests.map_tests import MapTesting
from src.maps.tree_map import TreeMap


class BinaryTreeTesting(MapTesting):
    """
    Класс для тестирования методов Binary Tree Map
    """
    t_test = TreeMap

    def test_less_in_left(self):
        """
        Проверяет, добавлен ли узел с меньшим ключом слева
        :return: None
        """
        self.map[8] = 'root'
        self.map[7] = 'left'
        self.assertEqual(self.map[7], self.map.root.left.value)

    def test_greater_in_right(self):
        """
        Проверяет, добавлен ли узел с большим ключом справа
        :return: None
        """
        self.map[8] = 'root'
        self.map[10] = 'right'
        self.assertEqual(self.map[10], self.map.root.right.value)

    def test_string_keys(self):
        """
        Проверяет, работает ли со строковыми ключами
        :return: None
        """
        self.map['b'] = 'root'
        self.map['a'] = 1
        self.assertEqual(self.map['a'], self.map.root.left.value)

    def test_del_leaf(self):
        """
        Проверяет удаление узла без дочерних элементов
        :return: None
        """
        self.map[5] = 'root'
        self.map[8] = 'right'
        self.map[4] = 'left'
        self.map[12] = 'right->right'
        del self.map[12]
        self.assertEqual(self.map.root.right.right, None)

    def test_del_node_with_one_child(self):
        """
        Проверяет удаление узла с одним дочерним элементом
        :return: None
        """
        self.map[33] = 'root'
        self.map[35] = 'right'
        self.map[5] = 'left'
        self.map[17] = 'left->right'
        self.map[18] = 'left->right->right'
        self.map[1] = 'left->left'
        self.map[4] = 'left->left->right'
        del self.map[17]
        self.assertEqual(self.map.root.left.right.value, self.map[18])
        del self.map[1]
        self.assertEqual(self.map.root.left.left.value, 'left->left->right')

    def test_del_node_with_two_children(self):
        """
        Проверяет удаление узла с обоими дочерними элементами
        :return: None
        """
        self.map[10] = 'root'
        self.map[7] = 'left'
        self.map[12] = 'right'
        self.map[9] = 'left->right'
        self.map[8] = 'left->right->left'
        self.map[6] = 'left->left'
        del self.map[7]
        self.assertEqual(self.map.root.left.value, 'left->right->left')
        self.assertEqual(self.map.root.left.right.value, 'left->right')
        self.assertIs(self.map.root.left.right.left, None)

    def test_del_root(self):
        """
        Проверяет удаление корня без едного, одного и двух дочерних элементов
        :return: None
        """
        self.map[1] = 'root'
        del self.map[1]
        self.assertEqual(self.map.root, None)
        self.map[1] = 'root'
        self.map[2] = 'right'
        del self.map[1]
        self.assertEqual(self.map.root.value, 'right')
        del self.map[2]
        self.map[1] = 'root'
        self.map[2] = 'right'
        self.map[0] = 'left'
        del self.map[1]
        self.assertEqual(self.map.root.value, 'right')
        self.assertEqual(self.map.root.left.value, 'left')
