import requests 
import json
import pprint 

url = f"https://restcountries.com/v3.1/name/China"

response = requests.get(url)

if response.status_code == 200: 
    # returns a data 
    data = json.loads(response.text)
    # current = response.json()
    with open("testing.json", "w") as fp:
        json.dump(data , fp, indent = 4)

else: 
    print(f'Error: {response.status_code}')