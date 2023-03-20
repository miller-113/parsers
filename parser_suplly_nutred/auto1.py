from main import get_data
import datetime


def main():
    global timer
    count = 1

    take_data_today = datetime.datetime.now().strftime("%d_%m")
    names_files = f'first_supply_nutrend'

    print(get_data(names_files))


if __name__ == '__main__':
    main()
