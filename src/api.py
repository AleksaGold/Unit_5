from typing import Any

import requests
from requests import Response, JSONDecodeError

from config import HH_URL_VACANCIES, EMPLOYERS, AREA, VACANCY_ONLY_WITH_SALARY
from src.exceptions import HhAPIException


class HhAPI:
    """Класс для работы с API hh.ru"""

    def __init__(self) -> None:
        """Конструктор для инициализации объекта"""
        self.__params = {
            'per_page': 100,
            'page': 0,
            'employer_id': EMPLOYERS,
            'area': AREA,
            'only_with_salary': VACANCY_ONLY_WITH_SALARY
        }

    @property
    def url(self) -> str:
        """Метод для получения базового url для подключения к API"""
        return HH_URL_VACANCIES

    def __get_response(self) -> Response:
        """Метод для получения запроса с сайта hh.ru"""
        return requests.get(self.url, params=self.__params)

    def get_response_vacancies(self) -> list[Any]:
        """Метод для получения вакансий с сайта hh.ru"""
        response = self.__get_response()
        status = self.__check_status(response)
        if not status:
            raise HhAPIException(f'Ошибка запроса данных status code: {response.status_code},'
                                 f' response: {response.text}')
        try:
            vacancies = []
            while self.__params.get('page') != 20:
                response_data = response.json()['items']
                vacancies.extend(response_data)
                self.__params['page'] += 1
            return vacancies
        except JSONDecodeError:
            raise HhAPIException(f'Ошибка получения данных,'
                                 f'получен не json-объект response: {response.text}')

    @staticmethod
    def __check_status(response: Response) -> bool:
        """Метод для получения статус кода запроса """
        return response.status_code == 200
