# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# *Наименование вакансии
# *Предлагаемую зарплату (отдельно мин. и и отдельно макс.)
# *Ссылку на саму вакансию
# *Сайт откуда собрана вакансия

import requests
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup
import lxml


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36'
vac_lst = []

vacancy = 'excel'
service = 'hh.ru'
#service = 'superjob.ru'
n_pages = 3

if service == 'hh.ru':
    base_url = 'https://hh.ru/'
    url = f'https://hh.ru/search/vacancy?st=searchVacancy&text={vacancy}&search_field=description&area=113&only_with_salary=true'
elif service == 'superjob.ru':
    base_url = 'https://www.superjob.ru/'
    url = f'https://www.superjob.ru/vacancy/search/?keywords={vacancy}'


def get_hh_vacancies(p_service, p_start_url, p_n_pages, p_vac_lst):
    page = 0
    page_url = p_start_url
    while page < p_n_pages:
        response = requests.get(page_url, headers={'User-Agent': USER_AGENT})
        soup = BeautifulSoup(response.text, 'lxml')
        body = soup.html.body
        res = body.findAll('div', attrs={'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

        for item in res:
            vac = {}
            vac['service'] = p_service
            vac['vacancy'] = item.find('a').text
            vac['url'] = item.find('a').attrs['href']
            compensation = item.find('div', attrs={'class': 'vacancy-serp-item__compensation'}).text
            if compensation.find('-') != -1:
                vac['min_compensation'] = re.sub('[^0-9]', '', compensation.split('-')[0])
                vac['max_compensation'] = re.sub('[^0-9]', '', compensation.split('-')[1])
            elif compensation.find('от') != -1:
                compensation = re.sub('[^0-9]', '', compensation)
                vac['min_compensation'] = compensation
                vac['max_compensation'] = compensation

            p_vac_lst.append(vac)

        page_url = f'{base_url}{body.find("a", attrs={"class": "bloko-button HH-Pager-Controls-Next HH-Pager-Control"}).attrs["href"]}'
        page += 1

def save_to_mongo(p_data):
    client = MongoClient('localhost', 27017)
    database = client.lesson2
    collection = database.jobs
    collection.insert_many(p_data)

get_hh_vacancies(service, url, n_pages, vac_lst)
save_to_mongo(vac_lst)




# result = body.findAll('h2', attrs={'data-marker':'bx-recommendations-block-title'})
# ads = body.findAll('div', attrs={'data-marker':'bx-recommendations-block-item'})
# urls = [f'{base_url}{item.find("a").attrs["href"]}' for item in ads]
#
# collection = database.avito
#collection.insert_many(list(map(req_ads, urls)))

# for item in urls:
#     result = req_ads(item)
#     collection.insert_one(result)

#time.sleep(random.randint(1, 5))

l=''
print(l)