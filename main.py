from config import config, EMPLOYERS
from src.DBManager import DBManager
from src.api import HhAPI
from src.utils import create_tables, get_employers, save_data_to_database


def main():
    """
    Функция для запуска основного кода программы
    :return:
    """
    hh = HhAPI()
    vacancies = hh.get_response_vacancies()
    employers = get_employers(EMPLOYERS)

    params = config()
    create_tables(params)
    save_data_to_database(employers, vacancies, params)

    data_base = DBManager(params)

    print("\nВведите ваш номер вашего запроса:\n"
          "1 - Список компаний и количество вакансий\n"
          "2 - Список всех вакансий\n"
          "3 - Список средней зарплаты по вакансиям\n"
          "4 - Список вакансий с зарплатой выше средней\n"
          "5 - Список вакансий с ключевым словом в названии вакансии\n")

    user_request = int(input())

    try:
        if user_request == 1:
            response_to_user_request = data_base.get_companies_and_vacancies_count()
            print(response_to_user_request)
            for row in response_to_user_request:
                print(row)
        elif user_request == 2:
            response_to_user_request = data_base.get_all_vacancies()
            print(response_to_user_request)
            for row in response_to_user_request:
                print(row)
        elif user_request == 3:
            response_to_user_request = data_base.get_avg_salary()
            print(response_to_user_request)
        elif user_request == 4:
            response_to_user_request = data_base.get_vacancies_with_higher_salary()
            print(response_to_user_request)
            for row in response_to_user_request:
                print(row)
        elif user_request == 5:
            keyword = input("Введите ключевое слово для поиска вакансий\n")
            response_to_user_request = data_base.get_vacancies_with_keyword(keyword)
            for row in response_to_user_request:
                print(row)
        else:
            print('Введен неверный запрос. Попробуйте снова')
    finally:
        data_base.cur.close()
        data_base.conn.close()


if __name__ == '__main__':
    main()
