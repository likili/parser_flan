import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool
import time


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
        price = soup.find('span', class_='main_price').text.strip()[6:-5].replace(' ', '')
    except:
        price = ''

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
            # a.text.strip()
            # art += ',"'+a+'"'
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

        # описания товара
        tab_content = []
        options = soup.find('div', class_='tab-content').find_all('div', class_='tab-pane')
        bv = ''
        for option in options:
            # option.text.strip()
            # tab_content += ',"' + option + '"'
            t = '</div><div>'
            for a in option.find_all('p'):
                a = a.find_all('span')

                for b in a:
                    t = t + b.text + '<br>'
                    # a = a.append(t)
                    # print(t)
            bv = t + '</div><div>'

            try:
                tb_contents = ''
                # r = 0
                table = option.find('table')
                for gd in table.find_all('tr'):

                    for td in gd.find_all('td'):
                        # td = td.text.strip()
                        # i = 1
                        # if i % 2 == 0:
                        tb_contents = tb_contents + '<td>' + td.text.strip() + '</td>'

                        # else:
                        #     tb_contents = tb_contents + td.text.strip()
                        # print(i + ':   ' + td)
                    # if r% 2 == 0:
                    #     tb_contents = tb_contents + '</tr><tr>'
                    # r += 1

                tb_contents = '<table><tbody><tr>' + tb_contents + '</tr></table></tbody>'

                # for a in option.find('table'):
                #     a = a.find_all('span')
                #     for b in a:
                #         t += b.text
                #         # a = a.append(t)
                #         # print(t)
                #
                # bv += t + "<br>"
            except:
                tb_contents = ''
            print(bv)
            bv = bv + tb_contents
            tab_content.append(bv)
    except:
        tab_content = ''

    try:
        img_links = []
        imgs = soup.find('ul', class_='thumbnails').find_all('li')#.find_all('a', class_='thumbnail')
        for img in imgs:
            a = img.find('a').get('href')  # где мы находим а внутри переменной img и забираем значение src строка возвращ
            img_links.append(a)
            print(a)
    except:
        img_links = ''
        # создаем словарь
    data = {
        'name': name,
        'art': art,
        'gabariti': gabariti,
        'tab_content': tab_content,
        'img_links': img_links,
        'price': price,
    }

    return data

def write_csv(data, file_name):
    name = file_name + '.csv'
    with open(
            # 'catalog.csv',
            # 'Настенные флорариумы FLANDRISS.csv',
            # 'Настенные чаши FLANDRISS.csv',
            # 'Подвесные флорариумы FLANDRISS.csv',
            # 'Панно.csv',
            # 'Настольные композиции.csv',
            # 'Композиции для FLANDRISS.csv',
             name,
            'a') as file:



        write = csv.writer(file)
        write.writerow((
            data['name'],
            data['art'],
            data['price'],
            data['gabariti'],
            data['tab_content'],
            data['img_links'],
        ))

        # print(data['price'])
        # print(data['name'], 'parsed')

def make_all(url):
    html = get_html(url)  # получаем html код страниц
    data = get_page_data(html)              # получаем необходимые теги со стринцы
    write_csv(data)                         #записываме в файл


def main():
    start = datetime.now()                      #старт времени  работы скрипта

    # # url = 'https://flandriss.ru/nastennie-fasadi-flandriss/?limit=100'                #Настенные флорариумы FLANDRISS
    # # url = 'https://flandriss.ru/podvesnie-chashi-/?limit=100'                         #Настенные чаши FLANDRISS
    # # url = 'https://flandriss.ru/1/?limit=100'                                         #Подвесные флорариумы FLANDRISS
    # # url = 'https://flandriss.ru/index.php?route=product/category&path=61'             #Панно
    # # url = 'https://flandriss.ru/zerkala-v-ramah/?limit=100'                           #Настольные композиции
    # url = 'https://flandriss.ru/index.php?route=product/category&path=62&limit=100'   #Композиции для FLANDRISS

    # 'https://flandriss.ru/nastennie-fasadi-flandriss/?limit=100',  # Настенные флорариумы FLANDRISS
    # 'https://flandriss.ru/podvesnie-chashi-/?limit=100',  # Настенные чаши FLANDRISS
    # 'https://flandriss.ru/1/?limit=100',  # Подвесные флорариумы FLANDRISS
    # 'https://flandriss.ru/index.php?route=product/category&path=61',  # Панно
    # 'https://flandriss.ru/zerkala-v-ramah/?limit=100',  # Настольные композиции
    # 'https://flandriss.ru/index.php?route=product/category&path=62&limit=100',  # Композиции для FLANDRISS


    # ссылки и имена файлов
    urls = [
        {
            'url': 'https://flandriss.ru/nastennie-fasadi-flandriss/?limit=100',
            'file_name': 'Настенные флорариумы FLANDRISS',
        },
        {
            'url': 'https://flandriss.ru/podvesnie-chashi-/?limit=100',
            'file_name': 'Настенные чаши FLANDRISS',
        },
        {
            'url': 'https://flandriss.ru/1/?limit=100',
            'file_name': 'Подвесные флорариумы FLANDRISS',
        },
        {
            'url': 'https://flandriss.ru/index.php?route=product/category&path=61',
            'file_name': 'Панно',
        },
        {
            'url': 'https://flandriss.ru/zerkala-v-ramah/?limit=10',
            'file_name': 'Настольные композиции',
        },
        {
            'url': 'https://flandriss.ru/index.php?route=product/category&path=62&limit=100',
            'file_name': 'Композиции для FLANDRISS',
        },
           ]

    for link in urls:
        time.sleep(20)
        all_links = get_all_links(get_html(link['url'])) # получаем все ссылки на товар с данной страницы


    # 0:00:18.143038
        for index, url in enumerate(all_links):     # где index - придуманный агрумента в который функция enumerate записывает значения нумерация опираций строк
            html = get_html(url)                    # получаем html код страниц
            data = get_page_data(html)              # получаем необходимые теги со стринцы
            write_csv(data, link['file_name'])                         #записываме в файл
            print(index)


#   много поточность где 20 колличество процессом оно может быть любое
#     map(funck, list) map работает как цикл фор он предает из списка list по одному значения и подставляет их в функуцию
#     для него создаем функцию make all
#     with Pool(40) as p:
#         p.map(make_all, all_links)
#
#
    end = datetime.now()                        #окончание времени  работы скрипта

    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()