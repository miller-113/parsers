# import csv
# import os
#
# import numpy as np
# import pandas
#
#
# def read_csv(file_name):
#     result = dict()
#     with open(f'{file_name}', encoding='utf8') as f1:
#         reader = csv.reader(f1)
#         for row in reader:
#             result.update(row)
#
#     return result
#
#
#
#
# path_to_parses_files = r'C:\Users\mille\Desktop\HW\\'
# # path_to_parses_files = r'\\192.168.1.11\Volume_1\Price\atlantmarket\\'
# old_file = path_to_parses_files + ''.join([file for file in os.listdir(path_to_parses_files) if 'first' in file and 'csv' in file])
# new_file = path_to_parses_files + ''.join([file for file in os.listdir(path_to_parses_files) if 'second' in file and 'csv' in file])
#
# a = read_csv(old_file)
# len(a)
# for i in a:
#     print(i)
# # for i in range(read_csv(len(old_file)[1:2])):
# #     print(i)

from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize('comp_cod.pyx'))