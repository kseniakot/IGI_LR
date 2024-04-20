import csv
import pickle
import zipfile
import os
from zipfile import ZipFile


class FileService:
    def __init__(self, file_path):
        """Initializes the FileService object with the given file path"""
        self._file_path = file_path

    @property
    def file_path(self):
        """Returns the file path of the FileService object"""
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        """Sets the file path of the FileService object"""
        self._file_path = value

    def file_exists(self):
        """Checks if the file exists"""
        return os.path.isfile(self._file_path)

    def read_csv(self):
        """Reads the data from the csv file and returns it as a dictionary"""
        if not self.file_exists():
            raise FileNotFoundError(f"The file {self._file_path} does not exist.")
        else:
            data = {}
            with open(self.file_path, 'r', encoding="utf-8", newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    data.update({row[0]: row[1:]})
            return data

    def write_csv(self, data):
        """Writes the data to the csv file"""
        with open(self.file_path, 'w', encoding="utf-8", newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            for country in data.keys():
                writer.writerow([country] + data[country])

    def read_pickle(self):
        """Reads the data from the pickle file and returns it as a dictionary"""
        if not self.file_exists():
            raise FileNotFoundError(f"The file {self._file_path} does not exist.")
        else:
            with open(self.file_path, 'rb') as file:
                return pickle.load(file)

    def write_pickle(self, data):
        """Writes the data to the pickle file"""
        with open(self.file_path, 'wb') as file:
            pickle.dump(data, file)

    def read_txt(self):
        """Reads the data from the txt file and returns it as a string"""
        if not self.file_exists():
            raise FileNotFoundError(f"The file {self._file_path} does not exist.")
        else:
            with open(self.file_path, 'r', encoding="utf-8") as file:
                return file.read()

    def write_txt(self, data):
        """Writes the data to the txt file"""
        with open(self.file_path, 'a', encoding="utf-8") as file:
            file.write(data)

    def clear_file(self):
        """Clears the contents of the given file"""
        with open(self.file_path, 'w') as file:
            pass


    @staticmethod
    def make_zip(zip_file_path, file_path):
        """Creates a zip file containing the file specified by the file_path property"""
        with ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(file_path)

    @staticmethod
    def get_zip_info(zip_file_path):
        """Returns the list of files in the zip file specified by the zip_file_path parameter"""
        with ZipFile(zip_file_path, 'r') as zip_file:
            return zip_file.infolist()

