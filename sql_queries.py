SQL_QUERIES = {
        "create_companies_table": """
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """,
        "create_vacancies_table": """
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                salary NUMERIC,
                company_id INTEGER REFERENCES companies(id)
            );
        """,
        "insert_company": """
            INSERT INTO companies (name) VALUES (%s) RETURNING id;
        """,
        "insert_vacancy": """
            INSERT INTO vacancies (title, salary, company_id) VALUES (%s, %s, %s);
        """,
        "get_companies_and_vacancies_count": """
            SELECT companies.name, COUNT(vacancies.id)
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.name;
        """,
        "get_all_vacancies": """
            SELECT companies.name, vacancies.title, vacancies.salary
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id;
        """,
        "get_avg_salary": """
            SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;
        """,
        "get_vacancies_with_higher_salary": """
            SELECT companies.name, vacancies.title, vacancies.salary
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE vacancies.salary > %s;
        """,
        "get_vacancies_with_keyword": """
            SELECT companies.name, vacancies.title, vacancies.salary
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE LOWER(vacancies.title) LIKE %s;
        """
    }