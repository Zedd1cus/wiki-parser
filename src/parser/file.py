"""
Модуль для работы с файлами
"""


def file_reader(filename: str):
    """Функция, считывающая строки в файле"""
    with open(filename, 'r', encoding='utf8') as file:
        line = file.readline()
        while line:
            yield line
            line = file.readline()


def list_writer(list_to_write: list, filename: str):
    """Функция, которая записывает в файл список, составленный из map"""
    with open(filename, 'w', encoding='utf8') as file:
        for key, value in list_to_write:
            file.write(f'{key} {value}\n')


def word_counter(words_list: list, word: str) -> int:
    """Подсчитывает, сколько слов встречается в списке слов"""
    result = 0
    for line in words_list:
        if not line:
            continue
        curr_word = line.split()[0]
        if curr_word == word:
            result += 1
    return result


def files_merge(*filenames: str, result_path: str):
    """
    Объединяет несколько файлов в один
    :param filenames: итерируемый с именами файлов
    :param result_path: файл, куда поместится результат
    :return: None
    """
    with open(result_path, 'w', encoding='utf8') as result_file:
        file_readers = [file_reader(filename) for filename in filenames]
        lines = [next(reader, None) for reader in file_readers]
        while any(lines):
            non_none_words = [word for word in lines if word]
            min_word_line = min(non_none_words, key=lambda _line: _line.split()[0])
            min_word = min_word_line.split()[0]
            # Если слово встречается несколько раз
            if word_counter(lines, min_word) > 1:
                next_indexes = []
                result_word_count = 0
                for line_index, line in enumerate(lines):
                    if not line:
                        continue
                    word, num = line.split()
                    if word == min_word:
                        result_word_count += int(num)
                        next_indexes.append(line_index)
                result_file.write(f'{min_word} {str(result_word_count)}\n')
                for next_index in next_indexes:
                    lines[next_index] = next(file_readers[next_index], None)
            # Если слово встречается только один раз
            else:
                result_file.write(f'{min_word_line}')
                next_index = lines.index(min_word_line)
                lines[next_index] = next(file_readers[next_index], None)


if __name__ == "__main__":
    pass
