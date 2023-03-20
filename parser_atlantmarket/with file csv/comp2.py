from comp_cod import *
import time
from contextlib import ExitStack

if __name__ == '__main__':
    with ExitStack() as stack:
        take_data_today = datetime.datetime.now().strftime("%d_%m")
        file_name = f'monitoring_atlantmarket{take_data_today}'
        path_to_parses_files = r'\\192.168.1.11\Volume_1\Price\atlantmarket\\'
        old_file = path_to_parses_files + ''.join(
            [file for file in os.listdir(path_to_parses_files) if 'second' in file and 'csv' in file])
        new_file = path_to_parses_files + ''.join(
            [file for file in os.listdir(path_to_parses_files) if 'first' in file and 'csv' in file])
        path_to_save = r'\\192.168.1.11\Volume_1\Price\\'
        print(checker_for_new_n_modified(old_file=old_file,
                                         new_file=new_file,
                                         monitoring_file=file_name,
                                         path=path_to_save
                                         ))

        close_files = stack.pop_all().close
