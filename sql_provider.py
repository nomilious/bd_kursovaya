import os
from string import Template


class SQLProvider:
    def __init__(self, file_path: str) -> None:
        self._scripts = {}
        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}').read())

    def get(self, name, **kwargs) -> str:
        if name in self._scripts:
            return self._scripts.get(name, '').substitute(**kwargs)  # подстановка параметров в запрос
        else:
            raise ValueError("Такого файла нету")
