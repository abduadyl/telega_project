import requests
from bs4 import BeautifulSoup
import json

def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text

def write_to_json(data):
    json_file = open('file_json.json', 'w')
    json.dump(data, json_file, indent=3)

def get_link(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='search-results-table').find('div', class_='table-view-list')
    all_pages = pages.find_all('div', class_='list-item')
    
    file1 = open('info_link.txt', 'w')
    for link in all_pages:
        url = 'https://www.mashina.kg'
        new_url = link.find('a').get('href')
        file1.write(url + new_url + '\n')
    file1.close()

def get_info_usd(html):
    soup = BeautifulSoup(html, 'lxml')
    usd = soup.find('div', class_='nbkr_tabs_wrapper').find('h2').text
    
    file2 = open('info_usd.txt', 'w')
    file2.write(usd)
    file2.close()

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='search-results-table').find('div', class_='table-view-list')
    all_pages = pages.find_all('div', class_='list-item')
    
    new_list = []
    for line in all_pages:
        try:
            #title
            title = line.find('a').find('h2').text
            title_result = title.split('\n')[1]
            title_result = title_result.strip()
        except:
            title = ''
        try:
            #price
            price = line.find('p', class_='price').text
            price_result = price.split('\n')
            price_result = price_result[1]
        except:
            price = ''
        try:
            #description
            description = line.find('div', class_='item-info-wrapper').text
            description_result = description.split('\n')
            description_result = [x.strip() for x in description_result]
            description_result = description_result[:9]
            description_result = ''.join(description_result)
        except:
            print()
        try:
            #photo
            photo = line.find('img').get('data-src')
        except:
            photo = ''

        data = {'title': title_result, 
                'price': price_result, 
                'description': description_result, 
                'photo': photo}
        
        new_list.append(data)
    write_to_json(new_list)

def main():
    url = 'https://www.mashina.kg/search/all/'
    url_usd = 'https://www.akchabar.kg/ru/exchange-rates/dollar/'
    get_page_data(get_html(url))
    get_link(get_html(url))
    get_info_usd(get_html(url_usd))

main()

