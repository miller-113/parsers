import datetime

import numpy
import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/13tokNIIBrWJQ1JWv-r9EPI3jM_7VS7ccVHI8nASK8Mk/edit?pli=1#gid=0'

def build_sheet_url(doc_id, sheet_id):
    return f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&id={sheet_id}'

def write_csv_to_local(df, file_path):
    df.to_csv(file_path, float_format="{:.0f}".format)
    # df.to_csv(file_path)

doc_id = '13tokNIIBrWJQ1JWv-r9EPI3jM_7VS7ccVHI8nASK8Mk'
sheet_id = '13tokNIIBrWJQ1JWv-r9EPI3jM_7VS7ccVHI8nASK8Mk&gid=0'
sheet_url = build_sheet_url(doc_id, sheet_id)


