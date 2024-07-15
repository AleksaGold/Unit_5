import requests
from requests import Response, JSONDecodeError

from config import HH_URL
from src.exceptions import HhAPIException


class HhAPI:
    """
    Класс для работы с API hh.ru
    """

    def __init__(self) -> None:
        self.__text = None
        self.__params = {
            'per_page': 100,
            'search_field': 'name'
        }

    @property
    def url(self) -> str:
        return HH_URL

    @property
    def get_text(self) -> str:
        return self.__text

    @get_text.setter
    def get_text(self, text: str) -> None:
        self.__text = text

    def __get_response(self) -> Response:
        if self.__text is None:
            raise HhAPIException('Поисковый запрос не задан ')
        self.__params['text'] = self.__text
        return requests.get(self.url, params=self.__params)

    def get_response_data(self) -> list[dict]:
        response = self.__get_response()
        status = self.__check_status(response)
        if not status:
            raise HhAPIException(f'Ошибка запроса данных status code: {response.status_code},'
                                 f' response: {response.text}')
        try:
            return response.json()
        except JSONDecodeError:
            raise HhAPIException(f'Ошибка получения данных,'
                                 f'получен не json-объект response: {response.text}')

    @staticmethod
    def __check_status(response: Response) -> bool:
        return response.status_code == 200

if __name__ == '__main__':
    hh = HhAPI()
    hh.get_text = 'python' # получить от пользователя через input
    data = hh.get_response_data()
    print(data)