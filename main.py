import requests
from bs4 import BeautifulSoup
import csv


CSV = 'cards.csv'
HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/cards/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.188 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0 jmBHNg')
    cards = []

    for item in items:
        cards.append(
            {
                'bank': item.find('div', class_='be80pr-16 be80pr-17 kpDSWu cxzlon').get_text(),
                'product': item.find('div', class_='be80pr-16 be80pr-17 kpDSWu cxzlon').find('a').get('href'),
                'element': item.find('a', class_='cpshbz-0 eRamNS').get_text(),
                'img_card': item.find('div', class_='be80pr-9 fJFiLL').find('img')
            }
        )
    return cards

def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Банк', 'Продукт', 'Элемент', 'Ссылка на картинку'])
        for item in items:
            writer.writerow([item['bank'], item['product'], item['element'], item['img_card']])

def parser():
    PAGENATION =input('Укажите колличество страниц: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
    else:
        print('Error')

parser()
