import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool


# from urllib.request import urlopen
# >>> from bs4 import BeautifulSoup
# >>> html = urlopen('https://beton24.ru/sochi/beton/')
# >>> bs = BeautifulSoup(html.read(), 'lxml')
# >>> result = bs.findAll("span", "catalog-index__link-text")[1]
# >>> result.text.replace(u'\xa0',' ').replace(u'\u2009', '')
# 'от 3836 ₽'


# получаем html текс с урлов
def get_html(url):
    # r = requests.get(url)
    r = urlopen(url)            #дает правильную кодировку
    print(r)
    return r

def get_all_links(html):
    soup = BeautifulSoup(html)
    # где 'lxml' тип парсера
    #  class_ надо всегда использовать с нижним подчеркиванием
    tags = soup.find('div', class_='row goods').find_all('div', class_='caption') #получаем все объекты soup

    links = [] #пока пустой список
    for tag in tags:
        a = tag.find('a').get('href') #где мы находим а внутри переменной tag и забираем значение href строка возвращ
        links.append(a)

    return links

# даные со страницы
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    # исключения лавушки для каждого тега
    try:
        # где .text.strip() переревести в строку и обрезать лишнее
        name = soup.find('div', id='content').find('h1').text.strip()
    except:
        name = ''

    try:
        # где .text.strip() переревести в строку и обрезать лишнее
        art = []
        arts = soup.find('ul', class_='prod_info').find_all('li') #find_all
        for a in arts:
            art.append(a.text.strip())
    except:
        art = ''
    try:
    #     class="gabariti"
        gabariti = soup.find('div', class_='gabariti').text.strip()
        print(gabariti)
    except:
        gabariti = ''
    try:
        tab_content = []
        options = soup.find('div', class_='tab-content').find_all('div', class_='tab-pane')
        for option in options:
            tab_content.append(option.text.strip())
    except:
        tab_content = ''

        # создаем словарь
    data = {
        'name': name,
        'art': art,
        'gabariti': gabariti,
        'tab_content': tab_content
    }

    return data

def write_csv(data):
    with open('catalog.csv', 'a') as file:

        write = csv.writer(file)
        write.writerow((
            data['name'],
            data['art'],
            data['gabariti'],
            data['tab_content'],
        ))

        print(data['name'], 'parsed')

def make_all(url):
    html = get_html(url)  # получаем html код страниц
    data = get_page_data(html)              # получаем необходимые теги со стринцы
    write_csv(data)                         #записываме в файл


def main():
    start = datetime.now()                      #старт времени  работы скрипта

    url = 'https://flandriss.ru/nastennie-fasadi-flandriss/?limit=100'

    all_links = get_all_links(get_html(url))


    # 0:00:18.143038
    # for index, url in enumerate(all_links):     # где index - придуманный агрумента в который функция enumerate записывает значения нумерация опираций строк
    #     html = get_html(url)                    # получаем html код страниц
    #     data = get_page_data(html)              # получаем необходимые теги со стринцы
    #     write_csv(data)                         #записываме в файл
    #     print(index)


    #много поточность где 20 колличество процессом оно может быть любое
    # map(funck, list) map работает как цикл фор он предает из списка list по одному значения и подставляет их в функуцию
    # для него создаем функцию make all
    with Pool(20) as p:
        p.map(make_all, all_links)


    end = datetime.now()                        #окончание времени  работы скрипта

    total = end - start
    print(str(total))




if __name__ == '__main__':
    main()