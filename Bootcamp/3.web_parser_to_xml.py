from openpyxl import Workbook
from bs4 import BeautifulSoup
import requests

work_book = Workbook()
work_sheet = work_book.active
web_page = requests.get('https://centersi.spb.ru/art/')
soup = BeautifulSoup(web_page.text, 'html.parser')
items = soup.find_all(class_='item-body')

for elem in items:
    title = elem.find(class_='item-name').text
    relative_url = elem.find(class_='playlist-inner-card__link').attrs['href']
    # url = 'https://live.skillbox.ru' + relative_url
    # row = [title, url]
    # print(row)
    # work_sheet.append(row)
    print(title)
work_book.save('Вебинары про Python от Skillbox.xlsx')
