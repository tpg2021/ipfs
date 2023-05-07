import ipfshttpclient
from flask import logging

hash = 'QmdKdYFRnSDpRhGv6GbW77N1bJWMRUYkY4mjyyRXARK2Su'

# Connect to your IPFS daemon
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

# Retrieve the file information from IPFS using the given hash
file_info = client.object.get(hash)

# Get the filename associated with the file by looking for the first "Name" field in the file's links
filename = next((link['Name'] for link in file_info['Links'] if 'Name' in link), None)

print(filename)