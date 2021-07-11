import io
import re
#import requests
import pdfplumber
import pandas as pd
from tabula import read_pdf
from tabulate import tabulate

# Doc file tren mang
# def download_file(url):
#     local_filename = url.split('/')[-1]

#     with requests.get(url) as r:
#         with open(local_filename, 'wb') as f:
#             f.write(r.content)

#     return local_filename

# invoice_url = 'Dia chi file pdf tren mang'
# inv_pdf = download_file(invoice_url)

file_path = 'Hoa_don.pdf'

# with open('Hoa_don_text_ver_1.txt', 'w') as f:
#     with pdfplumber.open(file_path) as pdf:
#         page = pdf.pages[0]
#         text = page.extract_text()
#         f.write(text)

with pdfplumber.open(file_path) as pdf:
    page = pdf.pages[0]
    text = page.extract_text()

# print(text)
# print(type(text))

# In vao text
with io.open('Hoa_don_text_ver_1.txt', 'w', encoding="utf-8") as f:
    f.write(text)
f.close()

# df = read_pdf("Hoa_don.pdf", pages=1)
# print(tabulate(df))
# print('----------------')
# type(tabulate(df))
