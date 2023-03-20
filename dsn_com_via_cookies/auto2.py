from main import *

if __name__ == '__main__':
    path_to_save = r'\\192.168.1.11\Volume_1\Price\dsn\\'
    # path_to_save = r'C:\Users\mille\Desktop\HW\\'
    file_name = 'second_dsn_dobavki'
    print(csv_writer(path=path_to_save, file_name=file_name))
