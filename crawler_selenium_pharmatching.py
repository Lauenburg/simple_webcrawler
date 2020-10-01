from selenium import webdriver
from csv_handler import create_csv_file, write_line_to_csv
from selenium.common.exceptions import NoSuchElementException
import re

# For javascript generated content that needs to be rendered on the DOM use selenium
# https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python/
# 26440563#26440563?newreg=833bb298f2c84c3281b729cbcfa2d421

# For a not deprecated headless chrome driver (install with home brew)
# https://stackoverflow.com/questions/50416538/python-phantomjs-says-i-am-not-using-headless

def crawl_main_page(url, max_pages, csv_file, csv_header):
    ''' Crawls over the main page defined by the URL

    :param url: Url that points to the main page
    :param max_pages: Number of pages to iterate over
    :param csv_file: Link to the file in which to save the information
    :param csv_header: Header of the csv file
    '''

    # Start page
    page = 1
    # Add page attribute to the url
    url = url+'?page='+str(page)

    # Request webpage
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    # start chrome browser
    browser = webdriver.Chrome(options=option)
    browser.get(url)

    # Iterate over the main list
    # Find all companies in the list
    for companys in browser.find_elements_by_class_name('company_overview'):
        speciality = None
        region = None

        for list_elements in companys.find_elements_by_tag_name('li'):
            try:
                speciality = list_elements.find_element_by_class_name('service_category icon')
                print(speciality)
            except NoSuchElementException:
                pass
            try:
                region = list_elements.find_element_by_class_name('region icon')
                print(region)
            except NoSuchElementException:
                pass

        if speciality is not None and region is not None:
            if 'Europ' in region and 'filling' in speciality:
                print('Jippi')




            print(re.sub('[\t]', '', str(list_elements.text.replace('\n', '')).strip()))
        '''
        for company in companys.findAll('div', {'class':'company_line indented clearboth'}):
            print('hello')
            # Check if the company is working in cosmetics
            # Check if the company operates in europe
            categorie = company.find('li',{'class','service_category icon'})
            area = company.find('li',{'class':'region icon'})
            print(categorie.text)
            print(area.text)
        '''

        #for special_tags in company.findAll('div',{'class', 'special_tags'}):
        #    for tag in special_tags.findAll()



    # Find the links to the "more detail" page




def company_spider(max_pages, path, csv_file, csv_header):
    ''' Crawls over a page and retrieves all the links defined with the "atributes" and "elements" below

    :param max_pages:
    :return:
    '''
    page = 1
    while page <= max_pages:
        url = 'https://www.cosmetic-business.com/tradefair/aussteller-produkte?page='+str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for link in soup.findAll('div',{'class':'list-item-content'}):
            for data in link.findAll('a'):
                #print(data)
                href = data.get('href')
                next_page = 'https://www.cosmetic-business.com' + href
            comp = get_single_item_data(next_page)
            if comp is not None:
                write_line_to_csv(path, csv_file, csv_header, comp)
                print(comp)

        page = page +1


def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    comp = {'name': None, 'webadress': None, 'adress': None}
    adress = soup.find('div', {'class','adress'})
    if adress is not None and 'Germany' in adress.text:
        #print((adress.text.replace('\n', '')).strip())
        comp = {'name': None, 'webadress': None, 'adress': None}
        comp['adress'] = re.sub('\s\s+', ' ', (adress.text.replace('\n', '')).strip())
        for counter, item_name in enumerate(soup.find_all('div', {'class':'tabbed-content clearfix'})):
            #print(item_name)
            h2 = item_name.h2
            h3 = item_name.h3
            if h2 is not None:
                h2 = re.sub('[\t]', '', str(h2.text.replace('\n', '')).strip())
                comp['name'] = h2
            elif h3 is not None and h2 != h3:
                h3 = re.sub('[\t]', '', str(h3.text.replace('\n', '')).strip())
                comp['name'] = h3
            if h2 is not None or h3 is not None:
                link = soup.find('div',{'class':'webadress'})
                link = link.text[20:]
                link = str(link.replace('\n', '')).strip()
                comp['webadress'] = str(link).split('\t')[0]
                return comp


if __name__ == '__main__':
    path = '/Users/lauenburg/Desktop/'
    csv_file = 'pharmatching'
    csv_header = ['name', 'webadress','adress']
    header = create_csv_file(path, csv_file)
    #company_spider(63, path, csv_file, csv_header)
    crawl_main_page('https://www.pharmatching.com/company/', 5, csv_file, csv_header)
