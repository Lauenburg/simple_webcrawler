import requests
from bs4 import BeautifulSoup
from csv_handler import create_csv_file, write_line_to_csv
import re


def company_spider(max_pages, path, csv_file, csv_header):
    ''' Crawls over a page and retrieves all the links defined with the "atributes" and "elements" below

    :param max_pages:
    :return:
    '''
    page = 1
    while page <= max_pages:
        url = 'https://www.wlw.de/de/firmen/kosmetik-lohnherstellung?page='+str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for comp_soup in soup.findAll('article',{'class':'panel panel--company'}):
            comp = {'name': None, 'webadress': None, 'adress': None}
            for link in comp_soup.findAll('a', {'class':'panel__logo'}):
                # print(data)
                href = link.get('href')
                next_page = 'https://www.wlw.de' + str(href)
                comp['adress'] = get_single_item_data(next_page)

            for data in comp_soup.findAll('div',{'class':'h4 panel__title'}):
                #print(data)
                name = data.a
                if name is not None:
                    comp['name'] = name.text
                    webadress = comp_soup.find('li', {'class': 'hidden-xs'})
                    # print(data)
                    if webadress is not None:
                        adress = webadress.a
                        if adress is not None:
                            comp['webadress'] = adress.text

                if comp is not None:
                    write_line_to_csv(path, csv_file, csv_header, comp)
                    print(comp)


        page = page +1


def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for adress_class in soup.findAll('p', {'class','company-address'}):
        a = adress_class.find('a')
        if a is not None:
            return a.text
        else:
            return ''


if __name__ == '__main__':
    path = '/Users/lauenburg/Desktop/'
    csv_file = 'werliefertwas_lohnabfüller'
    csv_header = ['name', 'webadress', 'adress']
    header = create_csv_file(path, csv_file)
    company_spider(4, path, csv_file, csv_header)
