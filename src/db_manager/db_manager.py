from typing import Optional

import psycopg2

from src.db_manager.base_manager import BaseManager


class DBManager(BaseManager):
    """
    Класс для работы с существующей БД.
    Объект класса DBManager позволяет:
        – получить список всех компаний и количество вакансий у каждой компании;
        – получить список всех вакансий с указанием названия компании, названия вакансии,
          зарплаты и ссылки на вакансию;
        – получить среднюю зарплату по всем вакансиям;
        – получить список вакансий с зарплатой выше средней;
        – получить список всех вакансий, в названии которых содержится переданное в метод слово.
    """

    def __init__(self, params: dict, db_name: str = "company_jobs_db") -> None:
        """
        Конструктор для инициализации объекта, работающего с БД.

        :param params: Параметры для соединения с БД.
        :param db_name: Название БД (опционально).
        """
        self.__params = params
        self.__db_name = db_name

    def _execute_query(self, query: str, query_values: Optional[tuple] = None) -> list[tuple]:
        """
        Подключается к БД и выполняет запрос.

        :param query: Запрос, который необходимо выполнить.
        :param query_values: Параметры запроса (опционально).
        :return: Данные полученные из БД.
        """
        with psycopg2.connect(dbname=self.__db_name, **self.__params) as conn:
            with conn.cursor() as cur:
                cur.execute(query=query, vars=query_values)
                fetched = cur.fetchall()

        conn.close()
        if isinstance(fetched, list):  # Проверка для mypy
            return fetched
        return [()]

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.

        :return: Данные полученные из БД.
        """
        query = """
            SELECT employers.employer_name, COUNT(*)
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            GROUP BY employer_name
            ORDER BY COUNT(*) DESC;
            """
        return self._execute_query(query)

    def get_all_vacancies(self) -> list[tuple]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.

        :return: Данные полученные из БД.
        """
        query = """
            SELECT employers.employer_name, vacancy_name, salary, vacancy_url
            FROM vacancies
            INNER JOIN employers USING(employer_id)
            ORDER BY salary DESC;
            """
        return self._execute_query(query)

    def get_avg_salary(self) -> list[tuple]:
        """
        Получает среднюю зарплату по всем вакансиям.

        :return: Данные полученные из БД.
        """
        query = "SELECT AVG(salary) FROM vacancies;"
        return self._execute_query(query)

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Получает список вакансий с зарплатой выше средней.

        :return: Данные полученные из БД.
        """
        query = """
            SELECT vacancy_name, salary, vacancy_url
            FROM vacancies
            WHERE salary > (SELECT AVG(salary) FROM vacancies)
            ORDER BY salary DESC;
            """
        return self._execute_query(query)

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """
        Получает список всех вакансий, в названии которых содержится переданное в метод слово.

        :param keyword: Слово, по которому выводятся вакансии.
        :return: Данные полученные из БД.
        """
        keyword = keyword.strip()
        if not keyword:
            raise ValueError("Слово, по которому должны выводиться вакансии, не было передано в метод объекта")
        kw_lower = f"%{keyword.lower()}%"
        kw_capitalize = f"%{keyword.capitalize()}%"

        query = """
            SELECT vacancy_name, salary, vacancy_url
            FROM vacancies
            WHERE vacancy_name LIKE %s
               OR vacancy_name LIKE %s
            ORDER BY salary DESC;
            """
        return self._execute_query(query, query_values=(kw_lower, kw_capitalize))

        # q1 = """
        #     SELECT vacancy_name, vacancy_url
        #     FROM vacancies
        #     WHERE vacancy_name ILIKE %s;
        #     """
        # return self._execute_query(q1, query_values=(keyword,))  # ILIKE не игнорирует регистр

        # q2 = """
        #     SELECT vacancy_name, vacancy_url
        #     FROM vacancies
        #     WHERE LOWER(vacancy_name) LIKE %s;
        #     """
        # return self._execute_query(q2, query_values=(kw_lower,))  # LOWER() не переводит слова в нижний регистр
