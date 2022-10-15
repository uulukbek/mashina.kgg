

import requests
from bs4 import BeautifulSoup as BS
import csv




def get_html(url):
    response = requests.get(url)
    return response.text


def get_soup(html):
    soup = BS(html, 'lxml')
    return soup

def get_data(soup): 
    catalog = soup.find('div', class_='table-view-list')
    cars = catalog.find_all('div', class_= 'list-item list-label')
    if cars:
        for car in cars:
            try:
                title = car.find('h2', class_='name').text.strip()
            except AttributeError:
                title = ''
                    # print(title)
            try: 
                price = car.find('strong').text
            except AttributeError:
                price = ''
                # print(price)
            try:
                image = car.find('img', class_='lazy-image').get('data-src')
            except AttributeError:
                image = ''
                # print(image)
            try:
                description = car.find('p', class_='year-miles').text.strip()+','+car.find('p',class_='body-type').text.strip()+','+car.find('p', class_='volume').text.strip()
            except AttributeError:
                description = ''
                # print(description)



            write_csv ({
                'title' : title,
                'image' : image,
                'price' : price,
                'description' : description
            })

    else:
        raise AttributeError ('Товары закончились')
        

def write_csv(data): 
    with open('cars.csv', 'a') as file :
        names = ['title','price','image','description']
        write = csv.DictWriter(file,delimiter=',',fieldnames=names)
        write.writerow(data)
        







def main(): 
    try:
        for i in range(1,30):
            BASE_URL = f'https://www.mashina.kg/commercialsearch/all/?type=3&page={i}' 
            print(f'Это {i} страница')
            html = get_html(BASE_URL)
            soup = get_soup(html)
            get_data(soup)
    except AttributeError:
        print('Товары закончились')

if __name__ =='__main__':
    main()


