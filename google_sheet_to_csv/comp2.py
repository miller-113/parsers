import os

from comp_cod import *
import time

if __name__ == '__main__':
    take_data_today = datetime.datetime.now().strftime("%d_%m")
    file_name = f'monitoring_google_sheet{take_data_today}'
    # path_to_parses_files = r'C:\Users\mille\Desktop\HW\\'
    path_to_parses_files = r'\\192.168.1.11\Volume_1\Price\google_sheet\\'
    old_file = path_to_parses_files + ''.join(
        [file for file in os.listdir(path_to_parses_files) if
         'second' in file and 'csv' in file])
    new_file = path_to_parses_files + ''.join(
        [file for file in os.listdir(path_to_parses_files) if
         'first' in file and 'csv' in file])
    path_to_save = r'\\192.168.1.11\Volume_1\Price\\'
    # path_to_save = r'C:\Users\mille\Desktop\HW\\'
    print(csv_writer(old_f=old_file,
                     new_f=new_file,
                     file_name=file_name,
                     file_path_to_save=path_to_save
                     ))
