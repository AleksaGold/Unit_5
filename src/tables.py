import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="Unit_5",
    user="postgres",
    port='5433',
    password="Agumod!11"
)
try:
    with conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS employers")
            cur.execute("DROP TABLE IF EXISTS vacancies")
            cur.execute(
                "CREATE TABLE employers(employer_id varchar(50) PRIMARY KEY,"
                "employer_name varchar(200) NOT NULL,"
                "employer_url text)"
            )
            cur.execute(
                "CREATE TABLE vacancies(vacancy_id varchar(50) PRIMARY KEY,"
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


