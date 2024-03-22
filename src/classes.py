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
        response = requests.get(self.url, params={'text': keyword, 'per_page': 100})
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
    def __init__(self, num, name, city, link, salary, requirement='Не указано', responsibility='Не указаны'):
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
        return f'Вакансия: {self.name}'

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
            if vacs['salary'] is None:
                vacs['salary'] = 0
            else:
                if vacs['salary']['from'] is None and vacs['salary']['to'] is not None:
                    vacs['salary'] = vacs['salary']['to']
                elif vacs['salary']['from'] is not None and vacs['salary']['to'] is None:
                    vacs['salary'] = vacs['salary']['from']
                elif vacs['salary']['from'] is not None and vacs['salary']['to'] is not None:
                    vacs['salary'] = vacs["salary"]["from"]
            vac0 = HHVacancies(num_vac, vacs['name'], vacs['area']['name'],
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
    def add_to_json(vacancy, file):
        with open(file, 'r+', encoding='utf=8') as f:
            file = json.load(f)
            file.append(vacancy)
            f.seek(0)
            json.dump(file, f, ensure_ascii=False, indent=4)

    @staticmethod
    def create_json(data, file_to_save):
        vacs_list = []
        for i in data:
            if i.responsibility is None:
                i.responsibility = 'Не указаны'
            if i.requirement is None:
                i.requirement = 'Не указаны'

            vacs_list.append({'Номер вакансии': i.num, 'Название вакансии': i.name, 'Город': i.city, 'Ссылка': i.link,
                           'Зарплата': i.salary, 'Требования': i.requirement, 'Обязанности': i.responsibility})

        with open(file_to_save, 'w', encoding='utf=8') as f:
            json.dump(vacs_list, f, ensure_ascii=False, indent=4)

    def delete_vacancies(self):
        pass

    @staticmethod
    def get_vacancies_by_filter(key_word, file):
        user_list = []
        with open(file, 'r', encoding='utf=8') as f:
            text = json.load(f)
        for i in text:
            if key_word in i['Название вакансии'] or key_word in i['Требования'] or key_word in i['Обязанности']:
                user_list.append(i)
        for vacs in user_list:
            for k, v in vacs.items():
                print(f'{k}:{v}')
            print()

    @staticmethod
    def sort_by_salary(n, file):
        with open(file, 'r', encoding='utf=8') as f:
            text = json.load(f)
            sorted_list = sorted(text, key=lambda x: x['Зарплата'], reverse=True)
            for i in sorted_list[0:n]:
                for k, v in i.items():
                    print(f'{k}:{v}')
                print()


