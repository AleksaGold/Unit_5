import psycopg2


class DBManager:
    """Класс для работы с данными в БД"""

    def __init__(self, params: dict):
        """Конструктор для инициализации объекта"""
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
         Метод для получения списка всех компаний и количества вакансий у каждой компании
        :return: список компаний
        """
        self.cur.execute(
            """SELECT employer_name, COUNT(vacancies.employer_id) as total_vacancies
            FROM employers
            JOIN vacancies USING(employer_id)
            GROUP BY employers.employer_name"""
        )
        return self.cur.fetchall()

    def get_all_vacancies(self) -> list[tuple]:
        """
        Метод для получения всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return: список вакансий
        """
        self.cur.execute(
            """SELECT employers.employer_name, vacancy_name, salary_from, salary_to, currency, vacancies_url
            FROM vacancies
            JOIN employers USING(employer_id)"""
        )
        return self.cur.fetchall()

    def get_avg_salary(self) -> list[tuple]:
        """
        Метод для получения средней зарплаты по вакансиям
        :return: среднюю зарплату по вакансиям
        """
        self.cur.execute(
            """SELECT AVG (salary_from) as avg_salary_from, AVG (salary_to) as avg_salary_to 
            FROM vacancies"""
        )
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Метод для получения всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: список вакансий
        """
        self.cur.execute(
            """SELECT vacancy_name, salary_from, salary_to, currency 
            FROM vacancies
            WHERE salary_from > (SELECT AVG (salary_from) FROM vacancies) 
            OR salary_to > (SELECT AVG (salary_to) FROM vacancies)"""
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword) -> list[tuple]:
        """
        Метод для получения всех вакансий, в названии которых содержатся переданные в метод слова
        :param keyword: ключевое слово для поиска вакансий
        :return: список вакансий
        """
        self.cur.execute(f"""SELECT * FROM vacancies 
                        WHERE vacancy_name LIKE '%{keyword}%' 
                        OR vacancy_name LIKE '%{keyword}' 
                        OR vacancy_name LIKE '{keyword}%' 
                        OR vacancy_name LIKE '{keyword.title()}%'
                        ORDER BY vacancy_name""")
        return self.cur.fetchall()
