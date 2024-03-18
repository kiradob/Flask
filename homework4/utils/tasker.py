from asyncio import create_task, gather
from multiprocessing import Process
from threading import Thread
from time import time

from utils.loader import URLImageLoader


class Tasker:

    @staticmethod
    def handle_urls_by_multithreading(url_list: list, path_to_save: str = './data/images') -> None:
        start_time = time()
        threads = []
# Обработка URL-адресов с использованием многопоточности
        for url in url_list:
            thread = Thread(target=URLImageLoader.get_image_from_url, args=(url, path_to_save))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print(f'Загрузка используя многопоточный подход завершилась за {time() - start_time:.2f} сек')

    @staticmethod
    def handle_urls_by_multiprocessing(url_list: list, path_to_save: str = './data/images') -> None:
        start_time = time()
        processes = []
# Обработка URL-адресов с использованием мультипроцессинга
        for url in url_list:
            process = Process(target=URLImageLoader.get_image_from_url, args=(url, path_to_save))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        print(f'Загрузка используя мультизадачный подход завершилась за {time() - start_time:.2f} сек')

    @staticmethod
    async def handle_urls_by_asynchronous(url_list: list, path_to_save: str = './data/images') -> None:
        start_time = time()
        tasks = []
# Обработка URL-адресов с использованием асинхронности
        for url in url_list:
            task = create_task(URLImageLoader.async_get_image_from_url(url, path_to_save))
            tasks.append(task)

        await gather(*tasks)

        print(f'Загрузка используя асинхронный подход завершилась за {time() - start_time:.2f} сек')