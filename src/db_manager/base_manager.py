from abc import ABC, abstractmethod


class BaseManager(ABC):
    """
    Абстрактный класс для работы с существующей БД.
    """

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Абстрактный метод получения списка всех компаний и количества вакансий у каждой компании.
        """
        pass

    @abstractmethod
    def get_all_vacancies(self) -> list[tuple]:
        """
        Абстрактный метод получения списка всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        """
        pass

    @abstractmethod
    def get_avg_salary(self) -> list[tuple]:
        """
        Абстрактный метод получения средней зарплаты по всем вакансиям.
        """
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Абстрактный метод получения списка вакансий с зарплатой выше средней.
        """
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """
        Абстрактный метод получения списка всех вакансий, в названии которых содержится переданное в метод слово.
        """
        pass
