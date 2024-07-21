import psycopg2

from config import HH_URL_EMPLOYERS


def get_employers(data: dict) -> list[dict]:
    """
    Функция для создания списка работодателей со ссылками
    :param data: словарь с парами id_работодателя: название компании
    :return: список работодателей
    """
    employers = []
    for employer_id, employer_name in data.items():
        employer_url = f'{HH_URL_EMPLOYERS}/{employer_id}'
        employer = {'employer_id': employer_id, 'employer_name': employer_name, 'employer_url': employer_url}
        employers.append(employer)
    return employers


def create_tables(params: dict) -> None:
    """
    Функция для создания таблиц в БД
    :param params: параметры для подключения к БД
    :return:
    """
    conn = psycopg2.connect(**params)

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS employers CASCADE")
                cur.execute("DROP TABLE IF EXISTS vacancies CASCADE")
                cur.execute(
                    "CREATE TABLE employers(employer_id varchar(50) PRIMARY KEY,"
                    "employer_name varchar(200) NOT NULL,"
                    "employer_url text)"
                )
                cur.execute(
                    "CREATE TABLE vacancies(vacancy_id SERIAL PRIMARY KEY,"
                    "vacancy_name varchar(200) NOT NULL,"
                    "salary_from integer,"
                    "salary_to integer,"
                    "currency varchar(5),"
                    "vacancies_url text,"
                    "employer_id varchar(50),"
                    "FOREIGN KEY (employer_id) REFERENCES employers(employer_id))"
                )
    finally:
        conn.close()


def save_data_to_database(employers: list[dict], vacancies: list[dict], params: dict) -> None:
    """
    Функция для заполнения таблиц в БД
    :param employers: список работодателей
    :param vacancies: список вакансий
    :param params: параметры для подключения к БД
    :return:
    """
    conn = psycopg2.connect(**params)

    try:
        with conn:
            for employer in employers:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO employers (employer_id, employer_name, employer_url)
                        VALUES (%s, %s, %s)
                        """,
                        (employer['employer_id'], employer['employer_name'], employer['employer_url'])
                    )
            for vacancy in vacancies:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO vacancies (vacancy_name, salary_from, salary_to, currency, vacancies_url, employer_id) 
                        VALUES (%s, %s, %s, %s, %s, %s) 
                        RETURNING vacancy_id
                        """,
                        (vacancy['name'], vacancy['salary']['from'], vacancy['salary']['to'],
                         vacancy['salary']['currency'], vacancy['alternate_url'], vacancy['employer']['id'])
                    )
    finally:
        conn.close()
