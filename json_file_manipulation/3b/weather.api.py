"""
transform to

{
    "New York": {
        "temperature": 22,
        "humidity": 55,
        "conditions": "Cloudy"
    },
    "London": {
        "temperature": 18,
        "humidity": 65,
        "conditions": "Rainy"
    },
    "Tokyo": {
        "temperature": 25,
        "humidity": 70,
        "conditions": "Sunny"
    }
}

"""

#--------------------------#
# Dummy fetch API function #
#--------------------------#

# import requests

#API_URL = "https://jsonplaceholder.typicode.com/posts"

#response = requests.get(API_URL)

# if response.status_code == 200:
#     data = response.json()  
# else:
#     print(f"Error: {response.status_code}")


import json
from collections import defaultdict

transformed_data = defaultdict(dict)

with open('api-data.json', 'r') as f:

    reader = json.load(f)

    for line in reader['data']:
        
        city = line["city"]
        t = line["temp_c"]
        h = line["humidity"]
        c = line["conditions"]

        transformed_data[city]["temperature"] = t
        transformed_data[city]["humidity"] = h
        transformed_data[city]["conditions"] = c

for k, v in transformed_data.items():
    print(k, v)
    print()

"""
New York {'temperature': 22, 'humidity': 55, 'conditions': 'Cloudy'}
London {'temperature': 18, 'humidity': 65, 'conditions': 'Rainy'}
Tokyo {'temperature': 25, 'humidity': 70, 'conditions': 'Sunny'}
"""
        