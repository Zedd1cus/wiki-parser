"""
Linked list.
Каждый узел имеет данные и ссылку на следующий узел.
"""


class LinkedElem:
    """
    Класс узлов с ссылками в одном направлении
    """
    def __init__(self, key, value=None, next_=None):
        self.key = key
        self.value = value
        self.next_ = next_

    def __str__(self):
        """
        Для использования HashMap
        :return: key: value string
        """
        return f'{self.key}:{self.value}'

    __repr__ = __str__

    def get_data(self):
        """
        Возвращает ключ и значение узла в кортеже
        :return: any_type
        """
        return self.key, self.value

    def has_next(self):
        """
        Указывает, имеет ли узел ссылку на следующий узел
        :return: bool
        """
        return self.next_ is not None


class LinkedList:
    """
    Linked list
    """
    def __init__(self, head):
        self.head = head
        self.length = 1
        self.tail = self.head
        self.iter = None

    def __iter__(self):
        self.iter = self.head
        return self

    def __next__(self):
        if self.iter is not None:
            res = self.iter
            iter_next = self.iter.next_
            self.iter = iter_next
            return res.key, res.value
        raise StopIteration

    def __str__(self):
        string_out = ''
        for key, value in self:
            string_out += f'({key}, {value})' + ' -> '
        return string_out[:-4]

    def input_data(self):
        """
        Добавляет новые элементы в хэш-карту.
        Пользователь вводит данные по всей консоли до тех пор, пока не будет выдана пустая строка.
        Каждая строка представляет собой элемент.
        :return: None
        """
        new_data = input()
        while new_data != '':
            new_key, new_value = new_data.split()
            self.add_data(new_key, new_value)
            new_data = input()
            self.length += 1

    def add_data(self, new_key, new_value):
        """
        Добавляет элемент в конец списка.
        :param new_key: data you want to add
        :param new_value: new value
        :return: None
        """
        self.tail.next_ = LinkedElem(new_key, new_value)
        self.tail = self.tail.next_

    def set_data(self, key, new_data):
        """
        Задает новое значение для узла
        :param key: key
        :param new_data: new value
        :return: None
        """
        current = self.head
        while current is not None and current.key != key:
            current = current.next_
        if current is None:
            raise KeyError("Such key doesn't exist")
        current.value = new_data

    def print_list(self):
        """
        Выводит весь linked list
        :return: None
        """
        current = self.head
        while current is not None:
            print(current.key, current.value)
            current = current.next_

    def del_head(self):
        """
        Удаляет head
        :return: None
        """
        self.head = self.head.next_
        self.length -= 1

    def del_last(self):
        """
        Удаляет последний элемент
        :return: None
        """
        current = self.head
        last_index = 0  # made to pass pylint tests :)
        for elem_index in range(self.length - 2):
            last_index = elem_index
            current = current.next_
        current.next_ = None
        self.length -= 1
        last_index -= 1

    def del_first_by_key(self, key):
        """
        Удаляет первый найденный элемент с заданным значением
        :param key: value of element
        :return: None
        """
        current = self.head
        previous = LinkedElem(None)
        while current is not None and current.key != key:
            previous = current
            current = current.next_
        if current is not None:
            previous.next_ = current.next_
            del current
            self.length -= 1
        if previous.value is None:
            if self.head.next_ is not None:
                tmp = self.head.next_
                del self.head
                self.head = tmp
            else:
                self.head = None

    def del_all_by_key(self, key):
        """
        Удаляет каждый элемент с заданным значением
        :param key: value of element
        :return: None
        """
        current = self.head
        previous = LinkedElem(None)
        while self.head is not None and current.key == key:
            current = current.next_
            self.head = current
        while current is not None:
            if current.key == key:
                previous.next_ = current.next_
                self.length -= 1
            else:
                previous = current
            current = current.next_

    def ins_node(self, insert_key, insert_value, key):
        """
        Вставляет элемент перед элементом с заданным значением
        :param insert_key: value of inserted element
        :param insert_value: value of inserted element
        :param key: value of searchable element
        :return: None
        """
        current = self.head
        previous = LinkedElem(None)
        while current is not None and current.key != key:
            previous = current
            current = current.next_
        if current is not None:
            previous.next_ = LinkedElem(insert_key, insert_value, previous.next_)
            current.next_ = LinkedElem(insert_key, insert_value, current.next_)
            self.length += 2
        if previous.value is None:
            current = self.head
            self.head = LinkedElem(insert_key, insert_value, current)


if __name__ == '__main__':
    first = LinkedElem(1, 2)
    linked_list = LinkedList(first)
    linked_list.add_data('5', 5)
    linked_list.add_data('3', 5)
    linked_list.add_data('10', 10)
    print(linked_list)
    linked_list.del_first_by_key(1)
    print(linked_list)
    for el in linked_list:
        print(f'({el.key}, {el.value})', end=' -> ')