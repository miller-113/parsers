from datetime import datetime

from main import csv_writer

if __name__ == '__main__':
    time = datetime.now()
    file_name = 'totalfit_first'
    # path_to_parse = r'C:\Users\mille\Desktop\HW\\'
    path_to_parse = r'\\192.168.1.11\Volume_1\Price\totalfit\\'
    print(csv_writer(file_name=file_name, path=path_to_parse))
    print(datetime.now() - time)
