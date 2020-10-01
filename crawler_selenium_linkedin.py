from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from csv_handler import create_csv_file, write_line_to_csv
from selenium.common.exceptions import NoSuchElementException
import re
import time
import csv
import config

# For javascript generated content that needs to be rendered on the DOM use selenium
#https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python/26440563#26440563?newreg=833bb298f2c84c3281b729cbcfa2d421
# For a not deprecated headless chrome driver (install with home brew)
#https://stackoverflow.com/questions/50416538/python-phantomjs-says-i-am-not-using-headless

def crawl_main_page(url, path, csv_file_read, csv_file_write):
    ''' This crawler iterates through a list of links to linkedin profiles and
        scrapes the number of contacts those profiles have.

    :param url: Url that points to the main page
    :param path: General path to the files
    :param csv_file_read: Path to the file from which the data is read
    :param csv_file_write:     # Path to the file to which the data is writen
    :return:
    '''

    # You have two choices for scraping:

    # 1.
    # If you want to debug and see what is happening:
    # Defining which driver to use and where that driver can be found
    # driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    # 2.
    # If you want to go for speed an scrape in the background
    # Set Chrome option to headless
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    # Specifying the driver, its location and to use it headless
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=option)

    # Login to Linkedin
    driver.get(url);
    search_box = driver.find_element_by_name('session_key')
    search_box.send_keys(config.username)
    search_box = driver.find_element_by_name('session_password')
    search_box.send_keys(config.password)
    search_box.submit()

    # List to save all the information including number of contacts
    information_with_number_of_contacts = []
    line_number = 0

    # Opening and reading the CSV
    with open(path+csv_file_read+'.csv', mode='r') as file:
        reader = csv.DictReader(file)

        # Retrieving the header of the file
        header = reader.fieldnames
        print('Header: ', header)

        # Lopping over all the lines of the CSV
        for line in reader:
            print('Line Nr: ', line_number)
            line_number = line_number + 1
            # The reader returns an 'OrderedDict' but we require a 'dict'
            line = dict(line)

            # Search for Linkedin link
            try:
                driver.get(line['Linkedin'])
            except InvalidArgumentException:
                pass

            # Search in DOM structure for all HTML items with a class='t-16'
            for linkedin_header in driver.find_elements_by_class_name('t-16'):
                # Filter for the element that has the keyword "Kontackte" in their context
                if "Kontakte" in re.sub('[\t]', '', str(linkedin_header.text.replace('\n', '')).strip()):
                        contacts = re.sub('[\t]', '', str(linkedin_header.text.replace('\n', '')).strip())
                        line['#contacts'] = str(contacts)
                        # Append the contact information to the information from the CSV
                        information_with_number_of_contacts.append(line)
                        print(contacts)
        driver.quit()

        # Write to a new csv file
        # Create header for the csv file
        csv_header = header
        csv_header.append('#contacts')
        # Create the file
        create_csv_file(path, csv_file_write, csv_header)
        # Loop through the list that holds all the information and write to the csv
        for dic in information_with_number_of_contacts:
            print(dic)
            write_line_to_csv(path, csv_file_write, csv_header, dict(dic))

if __name__ == '__main__':
    # General path to the files
    path = '/Users/lauenburg/Desktop/'
    # Path to the file from which the data is read
    csv_file_read = 'Lando_Leads_Predicpro_Linkedin'
    # Path to the file to which the data is writen
    csv_file_write = 'Lando_Leads_Predicpro_Linkedin_with_contacts'

    crawl_main_page('https://www.linkedin.com/login', path, csv_file_read, csv_file_write)
