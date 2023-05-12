import json
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import lxml


URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
KEYWORDS = ['Python', 'Django', 'Flask']

def get_headers():
    return Headers(browser='firefox', os='win').generate()

SOURCE = requests.get(URL, headers=get_headers()).text

bs = BeautifulSoup(SOURCE, features='lxml')

articles_list = bs.find_all(class_='vacancy-serp-item__layout')


def sample(date):
    vacancy_list = []
    for article in articles_list:
        link = article.find('a')['href']
        try: 
            salary = article.find('span', {'data-qa':'vacancy-serp__vacancy-compensation'}).text
        except:
            salary = 'Нет данных!'
        company = article.find('a', class_='bloko-link bloko-link_kind-tertiary').text
        city = article.find('div',{'data-qa':'vacancy-serp__vacancy-address'}).text.split(',')[0]
        vacancy_list.append({
            'link': link,
            'salary': salary,
            'company': company,
            'city': city
             })
    return vacancy_list

def write(file):
    with open('date.json', 'w', encoding='utf-8') as f:
        data = json.dump(file, f, ensure_ascii=False, indent=2)
        return data

if __name__ == '__main__':
    art = sample(articles_list)
    write(art)
