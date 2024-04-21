class CountryManager:
    """A class to manage countries."""
    def __init__(self):
        """Initializes the list of countries."""
        self.countries = []

    def add_country(self, country):
        """Adds a country to the list of countries."""
        self.countries.append(country)

    def find_city(self, city_name):
        """ Finds a city by its name."""
        for country in self.countries:
            if city_name in country.cities:
                return country.name
        return None

    def sort_countries(self):
        """ Sorts the list of countries by their names."""
        self.countries.sort(key=lambda country: country.name)





