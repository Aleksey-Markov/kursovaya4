import json
import requests
from abc import ABC, abstractmethod


class API(ABC):
    """
    абстрактный класс
    """
    @abstractmethod
    def get_vacancies(*args, **kwargs):
        pass


class HeadHunter(API):
    """
    класс для подключения к сайту с помощью API
    и получения списка вакансий по ключевому слову
    """
    def __init__(self, url):
        self.url = url

    def get_vacancies(self, keyword):
        """
        получение списка вакансий в формате JSON
        :param keyword:
        :return:
        """
        response = requests.get(self.url, params={'text': keyword})
        return response.json()

    @staticmethod
    def save_to_json(data, file_to_save):
        """
        сохранение списка вакансий в файл
        :param data:
        :param file_to_save:
        :return:
        """
        with open(file_to_save, 'w', encoding='utf8') as q:
            json.dump(data, q, ensure_ascii=False, indent=4)


class HHVacancies:
    """
    класс для взаимодействия с вакансиями
    """
    def __init__(self, num, name, city, link, salary, requirement, responsibility):
        self.num = num
        self.name = name
        self.city = city
        self.link = link
        self.salary = salary
        self.requirement = requirement
        self.responsibility = responsibility

    def __repr__(self):
        return f'{self.num}, {self.name}, {self.city}, {self.link}, {self.salary}, {self.requirement}, {self.responsibility}'

    def __str__(self):
        return f'Вакансия: {self.name}, Зарплата: {self.salary["from"]}, Ссылка на вакансию'

    @staticmethod
    def sort_vacancies(data):
        """
        создает пронумерованный список объектов класса
        :param data:
        :return:
        """
        num_vac = 1
        vacancies = []
        with open(data, 'r', encoding='utf=8') as file:
            text = json.load(file)
        for vacs in text['items']:
            vac0 = HHVacancies(num_vac, vacs['name'], vacs['address'],
                               vacs['alternate_url'], vacs['salary'],
                               vacs['snippet']['requirement'], vacs['snippet']['responsibility'])
            vacancies.append(vac0)
            num_vac += 1
        return vacancies

    def __gt__(self, other):
        """
        позволяет сравнить две вакансии по зарплате
        :param other:
        :return: более оплачиваемую вакансию
        """
        if self.salary is not None and other.salary is not None:
            if self.salary['from'] > other.salary['from']:
                return self
            else:
                return other
        else:
            return 'Зарплата не указана'

    def validate_salary(self):
        """
        позволяет просмотреть данные о зарплате вакансии и валидировать их в случае если она не указана
        :return:
        """
        if self.salary is None:
            self.salary = 'Зарплата не указана'
            return self.salary
        if self.salary['to'] is None:
            return f"{self.salary['from']}"
        else:
            return f"{self.salary['from']} - {self.salary['to']}"


class JSONAbstract(ABC):
    def add_to_json(self, *args, **kwargs):
        pass

    def get_vacancies_by_filter(self, *args, **kwargs):
        pass

    def delete_vacancies(self, *args, **kwargs):
        pass


class JSON(JSONAbstract):
    @staticmethod
    def add_to_json(data):
        vacs_list = []
        for i in data:
            vacs_list.append({'Номер вакансии': i.num, 'Название вакансии': i.name, 'Город': i.city, 'Ссылка': i.link,
                           'Зарплата': i.salary, 'Требования': i.requirement, 'Обязанности': i.responsibility})

        with open('spisochek.json', 'w', encoding='utf=8') as f:
            json.dump(vacs_list, f, ensure_ascii=False, indent=4)

    def delete_vacancies(self):
        pass

    def get_vacancies_by_filter(self, *args, **kwargs):
        with open('vacancies.json', 'r', encoding='utf=8') as f:
            criterion = input('Выберите критерий для поиска по вакансиям: \nВведите "key" для поиска по ключевому слову\n'
                              'Введите "city" для поиска по городу\nВведите "money" для поиска по зарплате\n')
            if criterion == 'key':
                key = []
                key_word = input('Введите ключевое слово для поиска по вакансиям: \n')
                for i in f:
                    if key_word in i:
                        key.append(i)
                print(key)
            if criterion == 'city':
                cities = []
                city = input('Введите город для поиска по вакансиям: \n')
                for i in f:
                    if city in i:
                        cities.append(i)
                print(cities)
            if criterion == 'money':
                money = []
                salary = input('Введите зарплату для поиска по вакансиям: \n')
                for i in f:
                    if salary in i:
                        money.append(i)
                print(money)


v = HHVacancies.sort_vacancies('vacancies.json')
print(v)

q = JSON.add_to_json(v)
