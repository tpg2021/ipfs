import ipfshttpclient
from flask import logging
import PyPDF2 as pdf


#
# hash = 'QmdKdYFRnSDpRhGv6GbW77N1bJWMRUYkY4mjyyRXARK2Su'
#
# # Connect to your IPFS daemon
# client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
#
# # Retrieve the file information from IPFS using the given hash
# file_info = client.object.get(hash)
#
# # Get the filename associated with the file by looking for the first "Name" field in the file's links
# filename = next((link['Name'] for link in file_info['Links'] if 'Name' in link), None)
#
# print(filename)

def get_file_classifer_from_label(label: str):
    my_map = {'0': 'Insurance',
              '1': 'Mortgage'
              }
    return my_map.get(label)


def process_pdf(data):
    extracted_text = str()
    if data.filename.endswith('.pdf'):
        pdf_reader = pdf.PdfFileReader(data)
        num_pages = pdf_reader.numPages
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            extracted_text += page.extractText()
    return extracted_text
