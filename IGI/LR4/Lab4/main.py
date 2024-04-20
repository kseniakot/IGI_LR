# Ksenia Kotova 253503

class Country:
    def __init__(self, name, population, area):
        self.name = name
        self.population = population
        self.area = area

    def density(self):
        return self.population / self.area

    def __str__(self):
        return f'{self.name} (pop: {self.population}, area: {self.area})'


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
