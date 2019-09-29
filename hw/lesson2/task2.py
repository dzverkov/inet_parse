# На основе материалов урока, сделать выборку объявлений с AVITO по категории недвижимость квартиры продажа, сохраняем:
# Имя пользователя который опубликовал объявление
# Ссылку на профиль пользователя
# Параметры объявления (метраж, этаж, и тд)
# Стоимость
# Телефон (те кто сможет)
# url адрес объявления

import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import lxml
import time
import random


#mongo_url = 'mongo://login:pass@localhost:27017'

client = MongoClient('localhost', 27017)
database = client.lesson2

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36'


def req_ads(url):
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    soup = BeautifulSoup(response.text, 'lxml')
    try
        user = soup.body.find('div', attrs={'class':'seller-info-name'}).find('a').text.strip()
        user_profile = f'{base_url}{soup.body.find("div", attrs={"class":"seller-info-name"}).find("a").attrs.get("href")}'
    except  AttributeError:
        user = None
        user_profile = None
    try:
        price = soup.body.findAll('span', attrs={'class':'js-item-price', 'itemprop':'price'})[0].attrs.get('content')
    except IndexError:
        price = None

    result = {'title': soup.head.title.text,
              'user': user,
              'user_profile': user_profile,
              'price': int(price) if price and price.isdigit else None,
              'url': response.url,
              'params': [tuple(item.text.split(':')) for item in soup.body.findAll('li', attrs={'class':'item-params-list-item'})]
             }
    return result

base_url = 'https://www.avito.ru'
url = 'https://www.avito.ru/konakovo/kvartiry/prodam?cd=1'

page = 0
n_pages = 2
page_url = url
while page < n_pages:
    response = requests.get(page_url, headers={'User-Agent': USER_AGENT})

    soup = BeautifulSoup(response.text, 'lxml')
    body = soup.html.body
    result = body.findAll('h3', attrs={'data-marker':'item-title'})
    urls = [f'{base_url}{item.find("a").get("href")}' for item in result]

    collection = database.avito

    for item in urls:
         result = req_ads(item)
         collection.insert_one(result)

    page_url = f'{base_url}{body.find("a", attrs={"class":"js-pagination-next"}).attrs.get("href")}'
    page += 1


#time.sleep(random.randint(1, 5))
#print(l)