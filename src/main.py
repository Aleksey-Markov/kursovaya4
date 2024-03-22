from src.classes import HeadHunter, HHVacancies, JSON


def user_interaction():
    user_vacancy = input('Введите вакансию для поиска на сайте hh.ru: \n')
    hh = HeadHunter('https://api.hh.ru/vacancies')
    vacancies = hh.get_vacancies(user_vacancy)
    hh.save_to_json(vacancies, 'vacancies.json')
    sorted_vacs = HHVacancies.sort_vacancies('vacancies.json')
    file_vacs = JSON.create_json(sorted_vacs, 'user_vacancies.json')
    user_keyword = input('Введите ключевое слово для поиска по вакансиям: \n').title()
    print(JSON.get_vacancies_by_filter(user_keyword, 'user_vacancies.json'))
    salary_top = int(input('Введите количество вакансий отсортированных по зарплате:\n'))
    JSON.sort_by_salary(salary_top, 'user_vacancies.json')


user_interaction()
