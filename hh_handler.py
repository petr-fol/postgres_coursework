from db_manager import DBManager
import requests
import json


def get_vacancies_from_companies():
    # Список ID компаний
    company_ids = [
        '3918788', '592442', '1057', '6769', '7311',
        '232719', '5552641', '10013204', '6088189', '802184',
        '26624', '906557', '1790285', '9422712', '2381', '1373'
    ]

    # Создаем пустой список для хранения данных о вакансиях
    vacancies_data = []

    for company_id in company_ids:
        # Формируем URL запроса к API hh.ru для получения вакансий от конкретной компании
        url = f'https://api.hh.ru/vacancies?employer_id={company_id}&area=1&per_page=100'

        # Делаем GET-запрос к API
        response = requests.get(url, headers={'User-Agent': 'Your-App'})

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Преобразуем ответ в JSON
            data = response.json()

            # Добавляем данные о вакансиях в список
            vacancies_data.extend(data['items'])
        else:
            print(f"Ошибка при запросе данных для компании с ID {company_id}. Статус код: {response.status_code}")

    # Сохраняем данные в файл
    with open('vacancies_data.json', 'w', encoding='utf-8') as file:
        json.dump(vacancies_data, file, ensure_ascii=False, indent=2)


def get_company_id_by_name(company_name):
    url = f'https://api.hh.ru/employers'
    params = {'text': company_name}

    response = requests.get(url, params=params, headers={'User-Agent': 'Your-App'})

    if response.status_code == 200:
        data = response.json()
        if data['items']:
            return data['items'][0]['id']
        else:
            print(f"Компания с названием '{company_name}' не найдена на hh.ru.")
            return None
    else:
        print(
            f"Ошибка при запросе данных для компании с названием '{company_name}'. Статус код: {response.status_code}")
        return None
