from task1.country import Country
from task1.CountryManager import CountryManager
from Services.file_service import FileService
import os
from menu.menu import print_menu, navigate_menu, wait_for_key_press


# Data for task 1
data_countries = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Canada': ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton'],
    'Mexico': ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Toluca'],
    'Brazil': ['Sao Paulo', 'Rio de Janeiro', 'Salvador', 'Brasilia', 'Fortaleza'],
    'UK': ['London', 'Birmingham', 'Leeds', 'Glasgow', 'Sheffield'],
    'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice'],
    'Germany': ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt'],
    'Russia': ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Kazan'],
    'China': ['Beijing', 'Shanghai', 'Chongqing', 'Tianjin', 'Guangzhou'],
    'Japan': ['Tokyo', 'Yokohama', 'Osaka', 'Nagoya', 'Sapporo']
}

data_cities = ['New York', 'Rio de Janeiro', 'Birmingham', 'Houston', 'Shanghai',
               'Toronto', 'Moscow', 'Nice', 'Glasgow']


def input_city():
    """Asks the user to input a city"""
    return input('Enter a city to learn its country: ')


def print_city_country(countries, cities):
    """Prints the city and the country it is in"""
    for city in cities:
        print_city_info(countries, city)


def print_city_info(countries, city):
    """Prints info about the city input by the user"""
    country = countries.find_city(city)
    if country:
        print(f'{city} is in {country}')
    else:
        print(f'{city} is not in any of the given country')


def task_1_csv():
    """Serialize source data to a csv file and deserialize it back from the csv file"""
    os.system('clear')
    print_source_data()
    countries = CountryManager()
    file_service = FileService('task1/countries.csv')
    # Serialize the data to a csv file
    file_service.write_csv(data_countries)
    # Deserialize the data from the csv file
    for key, value in (file_service.read_csv().items()):
        countries.add_country(Country(key, value))
    file_service.read_csv()
    # Print the city and the country it is in (for each city from the source list)
    print_city_country(countries, data_cities)
    # Print info about the city input by the user
    city = input_city()
    print_city_info(countries, city)
    wait_for_key_press()


def task_1_pickle():
    """Serialize source data to a pickle file and deserialize it back from the pickle file"""
    os.system('clear')
    print_source_data()
    countries = CountryManager()
    file_service = FileService('task1/countries.pickle')
    # Serialize the data to a pickle file
    file_service.write_pickle(data_countries)
    # Deserialize the data from the pickle file
    for key, value in file_service.read_pickle().items():
        countries.add_country(Country(key, value))

    # Print the city and the country it is in (for each city from the source list)
    print_city_country(countries, data_cities)
    # Print info about the city input by the user
    city = input_city()
    print_city_info(countries, city)
    wait_for_key_press()


def task_1():
    """Task 1 menu"""
    os.system('clear')

    prompt = '\t\t\t\tWhat would you like to do?'
    tasks = {
        "Work with csv file": task_1_csv,
        "Work with pickle": task_1_pickle,
    }
    options = list(tasks.keys()) + ["Exit"]
    choice = 1

    print_menu(choice, options, prompt)
    navigate_menu(choice, options, prompt, tasks)


def print_source_data():
    """Print the source data"""
    print('Source city list:')
    for city in data_cities:
        print(city, end=', ')
    print()