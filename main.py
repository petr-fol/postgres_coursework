from db_manager import DBManager
from companies import companies
from hh_handler import get_vacancies_from_companies


def load_companies_to_db():
    for company_name, company_id in companies.items():
        DBManager.insert_company_with_id(company_name, company_id)


def load_vacancies_to_db(vacancies_data):
    # Загружаем компании, если их еще нет в базе
    # load_companies_to_db()

    for vacancy in vacancies_data:
        employer_id = vacancy.get("employer").get("id")

        # Получаем id компании из файла, если оно существует
        company_id = DBManager.get_company_id_by_employer_id(employer_id)

        if not company_id:
            # Если id компании не найден, пропускаем вакансию
            print(f"Не найден идентификатор для компании с employer_id {employer_id}")
            continue

        title = vacancy["name"]

        if vacancy["salary"] and vacancy["salary"]["from"] is not None:
            salary = vacancy["salary"]["from"]
        elif vacancy["salary"] and vacancy["salary"]["to"] is not None:
            salary = vacancy["salary"]["to"]
        else:
            salary = None

        # Добавляем вакансию
        DBManager.insert_vacancy(title, salary, company_id)


def print_menu():
    print("1. Получить список всех компаний и количество вакансий у каждой компании")
    print("2. Получить список всех вакансий")
    print("3. Получить среднюю зарплату по вакансиям")
    print("4. Получить список вакансий с зарплатой выше средней")
    print("5. Получить список вакансий по ключевому слову")
    print("6. Создать структуру базы данных")
    print("7. Загрузить вакансии в базу")
    print("8. загрузить компании в базу")
    print("0. Выйти")


def main():

    while True:
        print_menu()
        choice = input("Выберите действие (введите номер): ")

        if choice == "0":
            print("Выход из программы.")
            break
        elif choice == "1":
            companies_and_vacancies_count = DBManager.get_companies_and_vacancies_count()
            print("Список компаний и количество вакансий:")
            for company, count in companies_and_vacancies_count:
                print(f"{company}: {count} вакансий")
        elif choice == "2":
            all_vacancies = DBManager.get_all_vacancies()
            print("Список всех вакансий:")
            for company, title, salary in all_vacancies:
                print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary}")
        elif choice == "3":
            avg_salary = DBManager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {int(avg_salary)} рублей")
        elif choice == "4":
            vacancies_with_higher_salary = DBManager.get_vacancies_with_higher_salary()
            print("Список вакансий с зарплатой выше средней:")
            for company, title, salary in vacancies_with_higher_salary:
                print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary}")
        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            vacancies_with_keyword = DBManager.get_vacancies_with_keyword(keyword)
            print(f"Список вакансий с ключевым словом '{keyword}':")
            for company, title, salary in vacancies_with_keyword:
                print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary}")
        elif choice == "6":
            DBManager.create_database_structure()
            print("Структура базы данных успешно создана.")
        elif choice == "7":
            print("Выполняется . . .")
            json_file_data = get_vacancies_from_companies()
            load_vacancies_to_db(json_file_data)
            print("Вакансии успешно загружены.")
        elif choice == "8":
            print("Выполняется . . .")
            load_companies_to_db()
            print("Компании успешно загружены.")
        else:
            print("Неверный выбор. Пожалуйста, введите корректное значение.")


if __name__ == "__main__":
    main()
