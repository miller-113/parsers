from comp_cod import *

if __name__ == '__main__':
    data_t = datetime.datetime.now().strftime("%d_%m")
    file_name = f'monitoring_crm_dobavki{data_t}'
    # path_f = r'\\192.168.1.11\Volume_1\Price\crm_dobavki\\'
    path_f = r'C:/Users/mille/Desktop/HW/'
    old = path_f + ''.join([file for file in os.listdir(path_f) if
                            'first' in file and 'csv' in file])
    new = path_f + ''.join([file for file in os.listdir(path_f) if
                            'second' in file and 'csv' in file])

    # print(checker_for_new_n_modified(old, new, monitoring_file=file_name, path=r'\\192.168.1.11\Volume_1\Price\\'))
    print(checker_for_new_n_modified(old,
                                     new,
                                     monitoring_file=file_name,
                                     path='C:/Users/mille/Desktop/HW/'))