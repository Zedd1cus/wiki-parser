"""
Binary Search Tree.
Ключи узла слева и справа меньше, чем ключ родительского узла.
"""
from src.maps.base_map import BaseMap


class Node:
    """
    Узел TreeMap.
    Каждый узел имеет ключ, значение и ссылки на левый и правый узлы
    """
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def get_key(self):
        """Возвращает ключи узла"""
        return self.key

    def get_value(self):
        """Возвращает значения узла"""
        return self.key


class TreeMap(BaseMap):
    """
    Binary Search Tree class
    """
    def __init__(self, root=None):
        self.root = root
        self._size = 0

    def __setitem__(self, key, value):
        def set_node(node):
            if key > node.key:
                if node.right is None:
                    node.right = Node(key, value)
                else:
                    set_node(node.right)
            elif key < node.key:
                if node.left is None:
                    node.left = Node(key, value)
                else:
                    set_node(node.left)
            elif key == node.key:
                node.value = value
                self._size -= 1

        if self.root is None:
            self.root = Node(key, value)
        else:
            set_node(self.root)
        self._size += 1

    def __getitem__(self, key):
        def get_node(node):
            if node is None:
                raise KeyError('Such key does not exist')
            if key > node.key:
                return get_node(node.right)
            if key < node.key:
                return get_node(node.left)
            return node  # key == node.key
        return get_node(self.root).value

    def __delitem__(self, key):
        def del_node(node, key_, prev_node=None):
            if node is None:
                raise KeyError('Such key does not exist')
            if key_ > node.key:
                del_node(node.right, key_, node)
            elif key_ < node.key:
                del_node(node.left, key_, node)
            else:  # key == node.key
                if node.right is None and node.left is None:  # нет детей
                    if prev_node is not None:
                        if prev_node.right is node:  # "узел, подлежащий удалению" находится справа
                            prev_node.right = None
                        elif prev_node.left is node:  # "узел, подлежащий удалению, находится слева
                            prev_node.left = None
                elif node.right is None or node.left is None:  # один ребенок
                    child = node.right if node.right is not None else node.left
                    node.key = child.key
                    node.value = child.value
                    node.right = child.right
                    node.left = child.left
                else:  # два ребенка
                    curr = node.right
                    prev = node
                    while curr.left is not None:
                        prev = curr
                        curr = curr.left
                    # меняет k,v "узла, подлежащего удалению" на k,v наименьшего ключа в правом дереве
                    node.key = curr.key
                    node.value = curr.value
                    del_node(curr, curr.key, prev)  # del узел с наименьшим ключом в правом дереве

        if self.root is not None and self.root.right is None and self.root.right is None:
            self.root = None
        else:
            del_node(self.root, key)
        self._size -= 1

    def __iter__(self):
        def iter_node(node):
            if node is not None:
                yield node.key, node.value
                yield from iter_node(node.left)
                yield from iter_node(node.right)

        yield from iter_node(self.root)

    def clear(self):
        """Очищает TreeMap"""
        self.root = None
        self._size = 0

    def __str__(self):
        output = ''
        for key, value in self:
            output += f'({key} , {value})\n'
        return output

    __repr__ = __str__

    def __len__(self) -> int:
        return self._size


if __name__ == '__main__':
    tree = TreeMap()
    tree['root'] = 10
    print(list(tree.values()))
    del tree['root']
    print(list(tree.values()))