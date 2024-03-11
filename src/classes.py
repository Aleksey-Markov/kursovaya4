import json
import os
import requests
from abc import ABC, abstractmethod


class API(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunter(API):
    def __init__(self, url):
        self.url = url

    def get_vacancies(self, keyword):
        response = requests.get(self.url + '?text=' + keyword)
        return response.json()

    @staticmethod
    def save_to_json(data, file_to_save):
        with open(file_to_save, 'w', encoding='utf8') as q:
            json.dump(data, q, ensure_ascii=False, indent=4)


class HHVacancies:
    def __init__(self, name, city, link, salary, requirement, responsibility):
        self.name = name
        self.city = city
        self.link = link
        self.salary = salary
        self.requirement = requirement
        self.responsibility = responsibility


hh = HeadHunter('https://api.hh.ru/vacancies')
dat = hh.get_vacancies('Python')
files = hh.save_to_json(dat, 'vacancies.json')
print(dat['items'][0]['salary']['from'])
