from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from pprint import pprint

#_VACANCY = 'Phython'
_HH_LINK = 'https://hh.ru/search/vacancy'
_HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                 'AppleWebKit/537.36 (KHTML, like Gecko)'
                                 'Chrome/101.0.4951.67 Safari/537.36'}

class JobScrapper:
    ''' Main class '''

    def __init__(self, vacancy):
        ''' Constructor '''

        self.storage = list()
        self.vacancy = vacancy
        self._parse_vacancy

    def _parse_vacancy(self):
        ''' Vacancy parser'''

        self.storage.extend(self._vacancy_parse_hh())

    def _parse_hh(self):
        '''HH parser'''

        vacancies_info =[]

        params = {'text' : self.vacancy,
                  'search_input': 'name',
                  'page': ''}

        response = requests.get(_HH_LINK, params= params, headers= _HEADERS)

        if response.ok:
            soup = bs(response.text, 'html.parser')
            try:
                last_page = int(soup.find_all('a', {'data-qa': 'pager-page'})[-1].text)
            except:
                last_page = 1

        for page in range(0, last_page):
            params['page'] = page
            response = requests.get(_HH_LINK, params= params, headers= _HEADERS)
            if response.ok:
                soup = bs(response.text, 'html.parser')
                vacancies = soup.find('div', {'data-qa': 'vacancy-serp__results'}) \
                                .find_all('div', {'class': 'vacancy-serp-item'})
                for item in vacancies:
                    vacancies_info.append(self._vacancy_parse_hh(item))

    def _vacancy_parse_hh(self, vacancy):
        '''HH vacancy parser'''

        vacancy_info = {}

        vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
        vacancy_info['name'] = vacancy_name

        vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
        vacancy_info['link'] = vacancy_link

        vacancy_info['site'] = 'https://hh.ru'

        vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy_salary is None:
            min_salary = None
            max_salary = None
            currency = None
        else:
            vacancy_salary = vacancy_salary.getText()
            if vacancy_salary.startswith('до'):
                max_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                min_salary = None
                currency = vacancy_salary.split()[-1]

            elif vacancy_salary.startswith('от'):
                max_salary = None
                min_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                currency = vacancy_salary.split()[-1]

            else:
                max_salary = int("".join([s for s in vacancy_salary.split('–')[1] if s.isdigit()]))
                min_salary = int("".join([s for s in vacancy_salary.split('–')[0] if s.isdigit()]))
                currency = vacancy_salary.split()[-1]

        vacancy_info['max_salary'] = max_salary
        vacancy_info['min_salary'] = min_salary
        vacancy_info['currency'] = currency

        return vacancy_info

#scrapper = JobScrapper(_VACANCY)
#pprint(scrapper)


