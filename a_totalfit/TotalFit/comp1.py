from compare import *


if __name__ == '__main__':
    data_t = datetime.datetime.now().strftime("%d_%m")
    file_name = f'monitoring_tottalfit{data_t}'
    path_f = r'\\192.168.1.11\Volume_1\Price\totalfit\\'
    # path_f = r'C:\Users\mille\Desktop\HW\\'
    old = path_f + ''.join([file for file in os.listdir(path_f) if
                            'first' in file and 'csv' in file])
    new = path_f + ''.join([file for file in os.listdir(path_f) if
                            'second' in file and 'csv' in file])
    print(checker_for_new_n_modified(old, new,
                                     monitoring_file=file_name,
                                     path=r'\\192.168.1.11\Volume_1\Price\\'))

    # print(checker_for_new_n_modified(
    #     r"C:\Users\mille\Desktop\HW\totalfit_first.csv",
    #     r"C:\Users\mille\Desktop\HW\totalfit_second.csv",
    #     'monitoring_data',
    #     r"C:\Users\mille\Desktop\HW\\"))