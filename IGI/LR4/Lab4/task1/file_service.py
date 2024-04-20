import csv
import pickle


class FileService:
    def __init__(self, file_path):
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    def read_csv(self):
        data = {}
        with open(self.file_path, 'r', encoding="utf-8", newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                data.update({row[0]: row[1:]})
        return data

    def write_csv(self, data):
        with open(self.file_path, 'w', encoding="utf-8", newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            for country in data.keys():
                writer.writerow([country]+data[country])

    def read_pickle(self):
        with open(self.file_path, 'rb') as file:
            return pickle.load(file)

    def write_pickle(self, data):
        with open(self.file_path, 'wb') as file:
            pickle.dump(data, file)
