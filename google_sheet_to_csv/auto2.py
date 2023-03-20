from main import *

if __name__ == '__main__':
    file_name = 'second_google_sheet.csv'
    file_path = r'\\192.168.1.11\Volume_1\Price\google_sheet\\' + file_name
    # file_path = r'C:\Users\mille\Desktop\HW\\' + file_name

    df = pd.read_csv(sheet_url)
    write_csv_to_local(df, file_path)
    print(f'Файл: {file_name} создан в {file_path}')

