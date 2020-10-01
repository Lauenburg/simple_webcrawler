import requests
from bs4 import BeautifulSoup
from csv_handler import create_csv_file, write_line_to_csv
import re


def company_spider(max_pages, path, csv_file, csv_header):
    ''' Crawls over a page and retrieves all the links defined
        by the "attributes" and "elements" below

        Args
            max_pages: Number of pages of which to crawl
            path: General path for where the csv-file should be saved 
            csv_file: Name of the csv-file
            csv_header: Header for the csv
 
    :return:
        A dictionary containing the retrieved name, address and  
        web address.
    '''
    
    page = 1

    # main loop over the different pages of the webside
    while page <= max_pages:
        url = 'https://www.cosmetic-business.com/tradefair/aussteller-produkte?page='+str(page)
        # Retrieve the websites information and convert it according to BeautifulSoup's requirements 
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        # Iterate over the sides relevant elements to retrieve the links to relevant sub pages
        for link in soup.findAll('div',{'class':'list-item-content'}):
            for data in link.findAll('a'):
                href = data.get('href')
                subpage= 'https://www.cosmetic-business.com' + href
            # Function call to step in to sub pages and to retrieve the searched for information
            comp = get_single_item_data(next_page)
            # Write the information to the csv 
            if comp is not None:
                write_line_to_csv(path, csv_file, csv_header, comp)
                print(comp)

        page = page +1


def get_single_item_data(item_url):
    ''' Retrieves the name, the web address, and the address from
        the from the page item_url.
        
        Args:
            item_url: Link to the page from which to retrieve the data

    '''
    # Retrieve the websites information and convert it according to BeautifulSoup's requirements 
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    # Retrieve the name, the web address, and the address from the page item_url
    comp = None
    # First check if the address is German and if yes retrieve it and dickgo deeper 
    address = soup.find('div', {'class','address'})
    if address is not None and 'Germany' in address.text:
        comp = {'name': None, 'webaddress': None, 'address': None}
        comp['address'] = re.sub('\s\s+', ' ', (address.text.replace('\n', '')).strip())
        # Check either for the h2 or the h3 element (site specific) and retrieve it as the name
        for counter, item_name in enumerate(soup.find_all('div', {'class':'tabbed-content clearfix'})):
            h2 = item_name.h2
            h3 = item_name.h3
            if h2 is not None:
                h2 = re.sub('[\t]', '', str(h2.text.replace('\n', '')).strip())
                comp['name'] = h2
            elif h3 is not None and h2 != h3:
                h3 = re.sub('[\t]', '', str(h3.text.replace('\n', '')).strip())
                comp['name'] = h3
            # If a name exists, retrieve the web address and return all the information
            if h2 is not None or h3 is not None:
                link = soup.find('div',{'class':'webaddress'})
                link = link.text[20:]
                link = str(link.replace('\n', '')).strip()
                comp['webaddress'] = str(link).split('\t')[0]
                return comp
    return comp


if __name__ == '__main__':
    path = '/Users/lauenburg/Desktop/'
    csv_file = 'cosmetic_business'
    csv_header = ['name', 'webaddress','address']
    header = create_csv_file(path, csv_file)
    company_spider(63, path, csv_file, csv_header)
