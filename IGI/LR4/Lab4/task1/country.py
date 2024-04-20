class Country:
    def __init__(self, name, cities):
        """Initializes the country with its name and cities"""
        self.name = name
        self.cities = cities

    def __str__(self):
        """Returns the string representation of the country object"""
        return f'{self.name}: {self.cities}'
