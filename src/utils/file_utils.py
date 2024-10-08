import json
import os
from configparser import ConfigParser, NoSectionError
from typing import Generator

from config.paths import CONFIG_DIR, create_filepath


def config(filename: str = "database.ini", section: str = "postgresql") -> dict[str, str]:
    """
    Возвращает параметры подключения к базе данных.

    :param filename: Название конфигурационного файла (опционально). По умолчанию 'database.ini'.
    :param section: Название секции в конфигурационном файле (опционально) По умолчанию 'postgresql'.
    :raise FileNotFoundError: Если файл с указанным именем не найден.
    :raise NoSectionError: Если указанная секция не найдена в конфигурационном файле.
    :return: Словарь параметров соединения.
    """
    filepath = create_filepath(CONFIG_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл '{filename}' не найден")

    parser = ConfigParser()
    parser.read(filepath)

    if parser.has_section(section):
        ini_params = parser.items(section)
    else:
        raise NoSectionError(f"Секция '{section}' не найдена в файле {filename}")

    return dict(ini_params)


def employer_ids(filename: str = "employer_ids.json") -> Generator[int, None, None]:
    """
    Функция работающая с Json-файлами.
    Возвращает ID работодателей по одному в виде генератора.

    :param filename: Имя Json-файла, содержащего ID компаний (опционально).
    :raise FileNotFoundError: Если файл с указанным именем не найден.
    :return: Генератор, который возвращает ID работодателей по одному.
    """
    filepath = create_filepath(CONFIG_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл '{filename}' не найден")

    with open(filepath) as file:
        employer_ids_data = json.load(file)
        for employer_id in employer_ids_data:
            yield employer_id["id"]
