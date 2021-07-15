# Import thư viện cần thiết
import io
import os.path
import re
import requests
import pdfplumber
import argparse
import pandas as pd
from google_drive_downloader import GoogleDriveDownloader as gdd

#--------------------------------------------------------------#
# Thêm đối số dòng lệnh
"""
-f/ --file-path : đường dẫn đến file pdf (có thể là url )
"""
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file_path", required=True,
                help="path to pdf file")
args = vars(ap.parse_args())


# Đọc file pdf qua link url
# Nếu link url là link google sharing thì trả về fileID của file pdf
# Nếu link url dẫn đến file pdf thì trả về tên file
def download_file(url):
    download_name = url.split('/')
    local_filename = download_name[5]

    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)
    # print(download_name[5])
    # print(download_name)
    return local_filename


file_path = args["file_path"]


# Xử lý đường dẫn
if 'http' in file_path:
    print('Đây là đường dẫn URL\n-------------')
    if '.pdf' in file_path:
        print('Đã có định dạng pdf\n-------------')
        pdf_file = download_file(file_path)
    else:
        print('Chưa có định dạng pdf\n-------------')
        save_file = download_file(file_path)
        gdd.download_file_from_google_drive(
            file_id=save_file, dest_path='./Sample_Hoa_don_mua_hang.pdf')
        pdf_file = 'Sample_Hoa_don_mua_hang.pdf'

else:
    print('File có sẵn trên máy offline\n-------------')
    pdf_file = file_path

# print(pdf_file)
# print(file_path)

with pdfplumber.open(pdf_file) as pdf:
    page = pdf.pages[0]
    text = page.extract_text()

# print(text)
tax_idx = []
address = []
phone_num = []

# Lấy content theo cấu trúc có sẵn
for row in text.split('\n'):
    if row.startswith('Đơn vị bán hàng'):
        company_name = row
    elif row.startswith('Mã số thuế'):
        tax_idx.append(row)
    elif row.startswith('Địa chỉ'):
        address.append(row)
    elif row.startswith('Điện thoại'):
        phone_num.append(row)
    elif row.startswith('Đơn vị mua hàng'):
        customer_name = row
    elif row.startswith('Ngày'):
        date = row
    elif row.startswith('Tổng cộng'):
        price = 'Tổng tiền : ' + row.split(' ')[-1] + ' VND'

company_tax_idx = tax_idx[0]
company_add = address[0]
company_tele = phone_num[0]

customer_tax = tax_idx[1]
customer_add = address[1]
customer_tele = phone_num[1][:phone_num[1].find('H')]

content = (company_name + '\n' + company_tax_idx + '\n' +
           company_add + '\n' + company_tele + '\n' + date)

sign_content = (customer_name + ' _ ' + customer_tax + ' _ ' +
                customer_add + ' _ ' + customer_tele + ' _ ' + price)

# print(content)
# print('\n+++++++++++++++++++++++')
# print(sign_content)

# Lưu text file
# Lưu đặc trưng hóa đơn
save_path = 'data_for_pay_online_demo/content'
text_name = 'Hoa_don_' + customer_name.split(':')[-1] + '.txt'
# print(text_name)
complete_name = os.path.join(save_path, text_name)
with open(complete_name, 'w', encoding="utf-8") as f:
    f.write(content)
f.close()

# Lưu nội dung để ký
save_path_02 = 'data_for_pay_online_demo/sign_content'
sign_name = 'Signature_' + customer_name.split(':')[-1] + '.txt'
complete_name_02 = os.path.join(save_path_02, sign_name)
with open(complete_name_02, 'w', encoding="utf-8") as f:
    f.write(sign_content)
f.close()

# Lưu tên người viết hóa đơn
save_path_03 = 'data_for_pay_online_demo/writer'
writer_name = 'Written_by_' + company_name.split(':')[-1] + '.txt'
complete_name_03 = os.path.join(save_path_03, writer_name)
with open(complete_name_03, 'w', encoding="utf-8") as f:
    f.write(company_name.split(':')[-1])
f.close()


# import io
# import re
# import pdfplumber
# import pandas as pd

# file_path = 'Sample_Hoa_don.pdf'

# with pdfplumber.open(file_path) as pdf:
#     page = pdf.pages[0]
#     text = page.extract_text()

# print(text)
# # print(type(text))

# # In vao text
# with io.open('Hoa_don_text_ver_1.txt', 'w', encoding="utf-8") as f:
#     f.write(text)
# f.close()
