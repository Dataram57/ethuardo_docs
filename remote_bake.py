#================================================================
#Libs

import requests
import os
import json

#================================================================
#Config

config = json.load(open('remote_config.json', 'r'))

#================================================================
#Call
post_data = {
    'password': config['password']
    ,'command': 'B'
}
response = requests.post(config['address'], data = post_data)
print(response.text)