from compare_cod import checker_for_new_n_modified
import datetime
import os


def main():
    take_data_today = datetime.datetime.now().strftime("%d_%m")
    file_name = f'monitoring_nutrend_prod{datetime.datetime.now().strftime("%d_%m")}'

    old = ''.join([file for file in os.listdir('C:/Users/mille/Desktop/HW/') if
                   'second' in file and 'csv' in file])
    new = ''.join([file for file in os.listdir('C:/Users/mille/Desktop/HW/') if
                   'first' in file and 'csv' in file])

    print(checker_for_new_n_modified(old, new, monitoring_file=file_name))


if __name__ == "__main__":
    main()
