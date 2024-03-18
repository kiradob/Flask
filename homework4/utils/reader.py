class FileReader:
    """
    Читаем файл в список
    """

    @classmethod
    def read_file(cls, file_name) -> list:
        with open(file_name) as f:
            return f.readlines()