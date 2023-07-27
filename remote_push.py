import requests
import json


data = {
    'key1': 'value1',
    'key2': 'value2'
}
json_data = json.dumps(data)

headers = {
    'Content-Type': 'application/json',  # Set the appropriate content type if you are sending data
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # If your API requires authentication
    # Add any other headers as needed
}

response = requests.get('https://dataram57.com/ip', headers)
print(response.text)