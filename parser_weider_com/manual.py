import time

from main import csv_writer

while True:
    file_name = input('Введите название файла')
    print(csv_writer(file_name=file_name, mode='1'))
    time.sleep(5)