import requests 
import json
import pprint 

## FIRST API CALL 
# url = "https://api.yelp.com/v3/businesses/search"
# API_KEY = "dANgFspOWnetwW-iN3sAL7aaAn-QYjhlWfUitU19Duu5lARkYOgQI-Cee9JchHAgcDUUgaKxF4wvBmSRRQlZld-luauRenGua2DpxqBscI0KuD5ACsN6Y9BAcm3-ZXYx"
# client_ID = "NVFow3aK-2RZfpXZSc2-Ng"
# headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
# parameters = {"term": "restaurants",
#               "limit": 50,
#               "location": "Austin"}

# # get the requests 
# response = requests.get(url, headers = headers, params = parameters) 

# # print the text from the response object 
# if response.status_code == 200: 
#     print(response.text)
    
#     # returns a data 
#     data = json.loads(response.text)
#     pprint.pprint(data)
#     with open("yelp_menus.json", "w") as fp:
#         json.dump(data , fp, indent = 4) 

# else: 
#     print(f'Error: {response.status_code}')

## SECOND API CALL 
# url = "https://api.yelp.com/v3/businesses/search"
# API_KEY = "dANgFspOWnetwW-iN3sAL7aaAn-QYjhlWfUitU19Duu5lARkYOgQI-Cee9JchHAgcDUUgaKxF4wvBmSRRQlZld-luauRenGua2DpxqBscI0KuD5ACsN6Y9BAcm3-ZXYx"
# client_ID = "NVFow3aK-2RZfpXZSc2-Ng"
# headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
# parameters = {"term": "restaurants",
#               "limit": 50,
#               "offset": 50,
#               "location": "Austin"}

# # get the requests 
# response = requests.get(url, headers = headers, params = parameters) 

# # print the text from the response object 
# if response.status_code == 200: 
#     print(response.text)
    
#     # returns a data 
#     data = json.loads(response.text)
#     pprint.pprint(data)
#     with open("yelp_menus2.json", "w") as fp:
#         json.dump(data , fp, indent = 4) 

# else: 
#     print(f'Error: {response.status_code}')

## THIRD API CALL 
# url = "https://api.yelp.com/v3/businesses/search"
# API_KEY = "dANgFspOWnetwW-iN3sAL7aaAn-QYjhlWfUitU19Duu5lARkYOgQI-Cee9JchHAgcDUUgaKxF4wvBmSRRQlZld-luauRenGua2DpxqBscI0KuD5ACsN6Y9BAcm3-ZXYx"
# client_ID = "NVFow3aK-2RZfpXZSc2-Ng"
# headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
# parameters = {"term": "restaurants",
#               "limit": 50,
#               "offset": 100,
#               "location": "Austin"}

# # get the requests 
# response = requests.get(url, headers = headers, params = parameters) 

# # print the text from the response object 
# if response.status_code == 200: 
#     print(response.text)
    
#     # returns a data 
#     data = json.loads(response.text)
#     pprint.pprint(data)
#     with open("yelp_menus3.json", "w") as fp:
#         json.dump(data , fp, indent = 4) 

# else: 
#     print(f'Error: {response.status_code}')

## FOURTH API CALL 
# url = "https://api.yelp.com/v3/businesses/search"
# API_KEY = "dANgFspOWnetwW-iN3sAL7aaAn-QYjhlWfUitU19Duu5lARkYOgQI-Cee9JchHAgcDUUgaKxF4wvBmSRRQlZld-luauRenGua2DpxqBscI0KuD5ACsN6Y9BAcm3-ZXYx"
# client_ID = "NVFow3aK-2RZfpXZSc2-Ng"
# headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
# parameters = {"term": "restaurants",
#               "limit": 50,
#               "offset": 150,
#               "location": "Austin"}

# # get the requests 
# response = requests.get(url, headers = headers, params = parameters) 

# # print the text from the response object 
# if response.status_code == 200: 
#     print(response.text)
    
#     # returns a data 
#     data = json.loads(response.text)
#     pprint.pprint(data)
#     with open("yelp_menus4.json", "w") as fp:
#         json.dump(data , fp, indent = 4) 

# else: 
#     print(f'Error: {response.status_code}')

###### CREATE DICTIONARY OF AUSTIN RESTAURANTS #######
restaurants = {} 
restaurants["restaurants"] = []
north = [78727, 78728, 78753, 78758]
south = [78652, 78745, 78748]
west = [78730, 78732]
east = [78702, 78722, 78723, 78724]
central = [78701, 78702, 78703, 78704, 78705, 78712, 78722, 78731, 78741, 78746, 78751, 78752, 78756, 78757]

id = -1 

# iterate through all of the json files 
for i in range(1, 5):
    filename = f'yelp_menus{i}.json'
    file = open(filename)
    yelp_dict = json.load(file)
    

    # iterate through the response dictionary and select the data we want 
    for business in yelp_dict["businesses"]:
        id += 1 

        restaurants["restaurants"].append({})

        # unique ID for restaurant
        restaurants["restaurants"][id]["id"] = id        

        # get the restaurant's name 
        restaurants["restaurants"][id]["name"] = business["name"]

        # get the restaurant's image URL 
        restaurants["restaurants"][id]["image"] = business["image_url"]

        # get the restaurant's rating 
        restaurants["restaurants"][id]["rating"] = business["rating"]

        # get the restaurant's tags 
        restaurants["restaurants"][id]["tags"] = [] 
        for category in business["categories"]:
            restaurants["restaurants"][id]["tags"].append(category["title"])

        # get the restaurant's phone 
        restaurants["restaurants"][id]["phone"] = business["display_phone"]

        # get and determine the region of Austin 
        if int(business["location"]["zip_code"]) in north: 
            restaurants["restaurants"][id]["location"] = "North Austin"
        elif int(business["location"]["zip_code"]) in south: 
            restaurants["restaurants"][id]["location"] = "South Austin"
        elif int(business["location"]["zip_code"]) in east: 
            restaurants["restaurants"][id]["location"] = "East Austin"
        elif int(business["location"]["zip_code"]) in west: 
            restaurants["restaurants"][id]["location"] = "West Austin"
        else:
            restaurants["restaurants"][id]["location"] = "Central Austin"

# iterate through the restaurants dictionary and add cuisine to tag (if necessary), unique cuisine id, menu items, and menu items id 
filename2 = f'menu_items.json'
file2 = open(filename2)
menu_items_list = json.load(file2)
menu_items = menu_items_list["menu_items"]

filename3 = f'cuisines.json'
file3 = open(filename3)
cuisines_list = json.load(file3)
cuisines = cuisines_list["cuisines"]

# iterate through the entire list of restaurants 
for restaurant in restaurants["restaurants"]:
    restaurant["menu_items_id"] = [] 
    restaurant["menu_items"] = [] 

    restaurant["cuisine_id"] = [] 

    for cuisine in cuisines: 
        # restaurant is a part of this cuisine 
        if restaurant["id"] in cuisine["restaurant_id"]:
            restaurant["cuisine_id"].append(cuisine["id"])
            
            # all of the menu items in this cuisine will be linked to the restaurant 
            for index in range(len(cuisine["menu_items"])): 
                restaurant["menu_items_id"].append(cuisine["menu_id"][index])
                restaurant["menu_items"].append(cuisine["menu_items"][index])

            # make sure that the tag for the cuisine is the tag for restaurant id 
            if cuisine["name"] not in restaurant["tags"]: 
                restaurant["tags"].append(cuisine["name"])




# save restaurants to a json file 
with open("restaurants.json", "w") as fp:
    json.dump(restaurants , fp, indent = 4) 
