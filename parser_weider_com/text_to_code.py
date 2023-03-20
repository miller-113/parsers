import re

text = 'L-GLUTAMINE'
link = 'https://www.weider.com.ua/l-glutamine-victory/'
def get_cod_from_str(text: str, link, text1: str):
    link_text = re.sub('https://www.weider.com.ua/', '', link)
    split_text1 = re.split('[ :/-]', text)
    split_text2 = re.split('[ /-]', link_text)
    if text1 == '':
        text1 = '00'
    split_text = split_text1 + split_text2 + [text1]
    symbols = {
        "Aa": 1, "Аа": 27, "Щщ": 53,
        "Bb": 2, "Бб": 28, "Ъъ": 54,
        "Cc": 3, "Вв": 29, "Ыы": 55,
        "Dd": 4, "Гг": 30, "Ьь": 56,
        "Ee": 5, "Дд": 31, "Ээ": 57,
        "Ff": 6, "Ее": 32, "Юю": 58,
        "Gg": 7, "Ёё": 33, "Яя": 59,
        "Hh": 8, "Жж": 34, '1': '01',
        "Ii": 9, "Зз": 35, '2': '02',
        "Jj": 10, "Ии": 36, '3': '03',
        "Kk": 11, "Йй": 37, '4': '04',
        "Ll": 12, "Кк": 38, '5': '05',
        "Mm": 13, "Лл": 39, '6': '06',
        "Nn": 14, "Мм": 40, '7': '07',
        "Oo": 15, "Нн": 41, '8': '08',
        "Pp": 16, "Оо": 42, '9': '09',
        "Qq": 17, "Пп": 43, '0': '00',
        "Rr": 18, "Рр": 44,
        "Ss": 19,  "Сс": 45,
        "Tt": 20, "Тт": 46,
        "Uu": 21, "Уу": 47,
        "Vv": 22, "Фф": 48,
        "Ww": 23, "Хх": 49,
        "Xx": 24, "Цц": 50,
        "Yy": 25, "Чч": 51,
        "Zz": 26, "Шш": 52,
    }
    text_number = ''
    for item in split_text:
        if item == '':
            continue
        for value, key in symbols.items():
            if item[0] in value:
                text_number += str(key)
            if item[-1] in value:
                if item[0] == item[-1]:
                    continue
                text_number += str(key)

    return text_number

# print(get_cod_from_str('Бейсболка Trucker Cap Black/Red'))
# print(get_cod_from_str('Шапка Oxford Beanie Black'))
# print(get_cod_from_str('10 РROTEIN 80 PLUS', 'https://www.weider.com.ua/protein-80-plus/', 'БРАУНИ-ШОКОЛАД'))