import csv
import os


def create_csv_file(path, csv_file_name, csv_header=None):
    ''' Creates a csv file with the default header defined below.

        Args:
            path: Path to the csv_file
            csv_file_name: Name of the csv file
            csv_header: Header for the csv-file

        Return:
            The path to and the name of the created file and its header
    '''

    if csv_header is None:
        csv_header = ['name', 'webaddress', 'address']

    # Creates the file if it does not exist
    if not (os.path.isfile(path+csv_file_name+'.csv')):

        with open(path+csv_file_name+'.csv', 'w', newline='') as file:

            writer = csv.DictWriter(file, fieldnames=csv_header)

            writer.writeheader()

    return path, csv_file_name, csv_header


def write_line_to_csv(path, csv_file_name, header, csv_dictionary):
    ''' Open the csv-file and appends the dictionary.

        Args:
            path: Path to the location of the csv-file
            csv_file_name: Name of the csv-file
            header: Header of the csv-file
            csv_dictionary: The data that should be appended to the csv
    '''

    with open(path + csv_file_name + '.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writerow(csv_dictionary)




