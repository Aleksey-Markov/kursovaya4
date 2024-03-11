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


hh = HeadHunter('https://api.hh.ru/vacancies')
print(hh.get_vacancies('Python стажер'))