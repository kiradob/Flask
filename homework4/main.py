# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
# Каждое изображение должно сохраняться в отдельном файле,название которого соответствует названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: # image1.jpg
# Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.
import os
import sys
import platform

sys.path.append(os.path.abspath('utils/'))
from utils.parser import Parser
from utils.reader import FileReader
from utils.tasker import Tasker
from asyncio import run

url_list = []


if __name__ == '__main__':
    # Данные из командной строки
    url_list = Parser.cl_parser()
    # Если через командную строку ничего не передали, используем заготовку
    if len(url_list) == 0:
        url_list = [i.strip().replace('\n', '') for i in FileReader.read_file('data/images.lst')]

    print(f"{'-' * 20} Многопоточный подход {'-' * 20}")
    Tasker.handle_urls_by_multithreading(url_list, './data/images/multithreading')

    print(f"{'-' * 20} Мультизадачный подход {'-' * 20}")
    Tasker.handle_urls_by_multiprocessing(url_list, './data/images/multiprocessing')

    print(f"{'-' * 20} Асинхронный подход {'-' * 20}")
    run(Tasker.handle_urls_by_asynchronous(url_list, './data/images/asynchronous'))

    # Открывает проводник
    if platform.system() == 'Windows':
        os.system(f'explorer {os.path.abspath("data/images/")}')