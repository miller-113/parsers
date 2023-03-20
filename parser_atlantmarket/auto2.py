from contextlib import ExitStack

from main import *

if __name__ == '__main__':
    # path_to_save = r'C:\Users\mille\Desktop\HW\\'
    # file_name = 'second_atlantmarket'
    # with print(csv_writer(path_to_save, file_name)) as f:
    #     pass
    with ExitStack() as stack:
        # path_to_save = r'C:\Users\mille\Desktop\HW\\'
        path_to_save = r'\\192.168.1.11\Volume_1\Price\atlantmarket\\'
        file_name = 'second_atlantmarket'
        print(csv_writer(path_to_save, file_name))
        close_files = stack.pop_all().close
