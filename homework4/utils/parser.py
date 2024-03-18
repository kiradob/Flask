import argparse
from utils.reader import FileReader


class Parser:

    @staticmethod
    def cl_parser():
        parser = argparse.ArgumentParser(description='Обработка входящего списка URL адресов')
        parser.add_argument('-l', '--list', default=None,
                            help='Передайте строку с разделенными запятой URL адресами, указывающими на изображения.')
        parser.add_argument('-f', '--file', default=None,
                            help='Передайте файл с построчно хранящимися URL адресами, указывающими на изображения.')
        lst, file = parser.parse_args().list, parser.parse_args().file
        result = []
        if lst:
            result.extend([i.strip().replace('\n', '') for i in lst.split(',')])
        if file:
            result.extend([i.strip().replace('\n', '') for i in FileReader.read_file(file)])

        return result