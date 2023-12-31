import psycopg2
import os
from psycopg2 import sql
from sql_queries import SQL_QUERIES
# from companies import companies


class DBManager:

    @classmethod
    def _get_connection(cls):
        return psycopg2.connect(
            host="127.0.0.1",
            port="5432",
            database="CompanyVacancyDB",
            user="postgres",
            password=os.getenv("passwd_postgres"),
            client_encoding="utf-8"
        )

    @classmethod
    def create_database_structure(cls):
        # Используем контекстный менеджер для автоматического закрытия подключения
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            # Выполнение SQL-запросов
            cursor.execute(SQL_QUERIES["create_companies_table"])
            cursor.execute(SQL_QUERIES["create_vacancies_table"])

            # Фиксация изменений

    @classmethod
    def insert_company(cls, company_name):
        # Используем контекстный менеджер для автоматического закрытия подключения
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            # Выполнение SQL-запроса
            cursor.execute(SQL_QUERIES["insert_company"], (company_name,))

            # Получение ID вставленной компании

            # Фиксация изменений

    @classmethod
    def insert_vacancy(cls, title, salary, company_id):
        # Используем контекстный менеджер для автоматического закрытия подключения
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            # Выполнение SQL-запроса
            cursor.execute(SQL_QUERIES["insert_vacancy"], (title, salary, company_id))

            # Фиксация изменений

    @classmethod
    def get_companies_and_vacancies_count(cls):
        # Используем контекстный менеджер для автоматического закрытия подключения
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(SQL_QUERIES["get_companies_and_vacancies_count"])
            results = cursor.fetchall()

            return results

    @classmethod
    def get_all_vacancies(cls):
        # Используем контекстный менеджер для автоматического закрытия подключения
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(SQL_QUERIES["get_all_vacancies"])
            results = cursor.fetchall()

            return results

    @classmethod
    def get_avg_salary(cls):
        # Используем контекстный менеджер для автоматического закрытия подключения
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(SQL_QUERIES["get_avg_salary"])
            avg_salary = cursor.fetchone()[0]

            return avg_salary

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        # Используем контекстный менеджер для автоматического закрытия подключения
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            avg_salary = cls.get_avg_salary()

            cursor.execute(SQL_QUERIES["get_vacancies_with_higher_salary"], (avg_salary,))
            results = cursor.fetchall()

            return results

    @classmethod
    def get_vacancies_with_keyword(cls, keyword):
        # Используем контекстный менеджер для автоматического закрытия подключения
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(SQL_QUERIES["get_vacancies_with_keyword"], ('%' + keyword.lower() + '%',))
            results = cursor.fetchall()

            return results

    @classmethod
    def get_company_id_by_employer_id(cls, employer_id):
        query = """
            SELECT id
            FROM companies
            WHERE id = %s;
        """
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (employer_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    @classmethod
    def check_vacancy_exists(cls, title, company_id):
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT COUNT(*) FROM vacancies WHERE title = %s AND company_id = %s;"
            cursor.execute(query, (title, company_id))
            count = cursor.fetchone()[0]

            return count > 0

    @classmethod
    def insert_company_with_id(cls, company_name, company_id):
        with cls._get_connection() as conn:
            cursor = conn.cursor()

            # Проверяем, существует ли компания с указанным id
            # existing_company_id = cls.get_company_id_by_id(company_id)
        # for company in companies:
            # Если компании с таким id нет, добавляем новую
            query = sql.SQL("INSERT INTO companies (id, name) VALUES (%s, %s)")
            cursor.execute(query, (company_id, company_name))

    @classmethod
    def get_company_id_by_id(cls, company_id):
        with cls._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_QUERIES["get_company_id_by_id"], (company_id,))
            result = cursor.fetchone()
            return result[0] if result else None
