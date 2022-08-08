#https://spb.hh.ru/search/vacancy?text=Phyton&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true

#headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from pprint import pprint

page = 0
main_url = 'https://spb.hh.ru'
params = {'text' : 'Phyton',
         'salary' : '',
         'currency_code' : 'RUR',
         'experience' : 'doesNotMatter',
         'order_by' : 'relevance',
         'search_period' : '0',
         'items_on_page' : '20',
         'page' : page}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            'AppleWebKit/537.36 (KHTML, like Gecko)'
            'Chrome/101.0.4951.67 Safari/537.36'}

response = requests.get(main_url + '/search/vacancy', headers= headers, params= params)
with open('page.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

html = ''
with open('page.html', 'r', encoding='utf-8') as f:
    html = f.read()

#print(html)

soup = bs(html, 'html.parser')

vacancy_serp_item = soup.find_all('div', {'class': 'vacancy-serp-item'})
#print(len(vacancy_serp_item))

all_vacancy = []

try:
    last_page = int(soup.find_all('a',{'data-qa':'pager-page'})[-1].text)
except:
    last_page = 1

for i in range(last_page):
    for vacancy in vacancy_serp_item:
        index = 0
        vacancy_info = {}

        vacancy_anchor = vacancy.find('a')
        for i in vacancy_anchor:
            vacancy_name = vacancy_anchor.getText()
            vacancy_info['name'] = vacancy_name
            vacancy_link = vacancy_anchor.get('href')
            vacancy_info['link'] = vacancy_link

        vacancy_info['site'] = main_url + '/'

        vacancy_salary = vacancy.find('span', {'data-qa' : 'vacancy-serp__vacancy-compensation'})
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

        #vacancy_anchor = vacancy.find('span', {'data-qa' : 'vacancy-serp__vacancy-compensation'})
        #try:
            #for i in vacancy_anchor:
                #vacancy_salary = vacancy_anchor.getText()
                #vacancy_info['salary'] = vacancy_salary
        #except TypeError:
            #vacancy_salary = None
            #vacancy_info['salary'] = vacancy_salary

        all_vacancy.append(vacancy_info)

    params['page'] += + 1
    response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
    #print(len(all_vacancy))

all_vacancy_df = pd.DataFrame(all_vacancy)

#all_vacancy_df.to_csv('all_vacancy.csv', sep = ',', index = False)
all_vacancy_df.to_json('all_vacancy.json')