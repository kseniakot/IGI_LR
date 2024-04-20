class CountryManager:
    def __init__(self):
        self.countries = []

    def add_country(self, country):
        self.countries.append(country)

    def find_city(self, city_name):
        for country in self.countries:
            if city_name in country.cities:
                return country.name
        return None

    def sort_countries(self):
        self.countries.sort(key=lambda country: country.name)





