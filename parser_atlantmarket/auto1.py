from main import *
from contextlib import ExitStack

if __name__ == '__main__':
    with ExitStack() as stack:
        path_to_save = r'C:\Users\mille\Desktop\HW\\'
        # path_to_save = r'\\192.168.1.11\Volume_1\Price\atlantmarket\\'
        file_name = 'first_atlantmarket'
        print(csv_writer(path_to_save, file_name))
        close_files = stack.pop_all().close
