from models import app, db, Restaurant, Cuisine, MenuItem, restaurant_cuisine, menu_item_cuisine
import requests 
import json 


def load_json(filename):
    """
    Load a JSON file and return its content as a Python dict.
    """
    with open(filename, 'r') as file:
        return json.load(file)

''' NOTE: ALL OF THE DATA SCRAPING AND CLEANING IS COMMENTED OUT IN ORDER TO NOT SLOW DOWN THE SCRIPT (prof suggestion), but code is in Create_db (Harshul suggestion) '''

''' CALL THE EXTERNAL APIS WITHIN CREATE_DB '''
# def call_apis(): 
#     #### YELP API COLLECTION #### 
#     ## First API Call 
#     url = "https://api.yelp.com/v3/businesses/search"
#     API_KEY = "dANgFspOWnetwW-iN3sAL7aaAn-QYjhlWfUitU19Duu5lARkYOgQI-Cee9JchHAgcDUUgaKxF4wvBmSRRQlZld-luauRenGua2DpxqBscI0KuD5ACsN6Y9BAcm3-ZXYx"
#     client_ID = "NVFow3aK-2RZfpXZSc2-Ng"
#     headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
#     parameters = {"term": "restaurants",
#                 "limit": 50,
#                 "location": "Austin"}
    
#     # get the requests 
#     response = requests.get(url, headers = headers, params = parameters) 

#     # print the text from the response object 
#     if response.status_code == 200: 
        
#         # returns a data 
#         data = json.loads(response.text)
#         with open("yelp_menus1.json", "w") as fp:
#             json.dump(data , fp, indent = 4) 

#     else: 
#         print(f'Error: {response.status_code}')

#     ## Second API Call 
#     url = "https://api.yelp.com/v3/businesses/search"
#     API_KEY = "dANgFspOWnetwW-iN3sAL7aaAn-QYjhlWfUitU19Duu5lARkYOgQI-Cee9JchHAgcDUUgaKxF4wvBmSRRQlZld-luauRenGua2DpxqBscI0KuD5ACsN6Y9BAcm3-ZXYx"
#     client_ID = "NVFow3aK-2RZfpXZSc2-Ng"
#     headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
#     parameters = {"term": "restaurants",
#                   "limit": 50,
#                   "offset": 50,
#                   "location": "Austin"}

#     # get the requests 
#     response = requests.get(url, headers = headers, params = parameters) 

#     # print the text from the response object 
#     if response.status_code == 200: 
        
#         # returns a data 
#         data = json.loads(response.text)
#         with open("yelp_menus2.json", "w") as fp:
#             json.dump(data , fp, indent = 4) 

#     ## Third API Call 
#     url = "https://api.yelp.com/v3/businesses/search"
#     API_KEY = "dANgFspOWnetwW-iN3sAL7aaAn-QYjhlWfUitU19Duu5lARkYOgQI-Cee9JchHAgcDUUgaKxF4wvBmSRRQlZld-luauRenGua2DpxqBscI0KuD5ACsN6Y9BAcm3-ZXYx"
#     client_ID = "NVFow3aK-2RZfpXZSc2-Ng"
#     headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
#     parameters = {"term": "restaurants",
#                 "limit": 50,
#                 "offset": 100,
#                 "location": "Austin"}

#     # get the requests 
#     response = requests.get(url, headers = headers, params = parameters) 

#     # print the text from the response object 
#     if response.status_code == 200: 

#         # returns a data 
#         data = json.loads(response.text)
#         with open("yelp_menus3.json", "w") as fp:
#             json.dump(data , fp, indent = 4) 

#     ## Fourth API Call
#     url = "https://api.yelp.com/v3/businesses/search"
#     API_KEY = "dANgFspOWnetwW-iN3sAL7aaAn-QYjhlWfUitU19Duu5lARkYOgQI-Cee9JchHAgcDUUgaKxF4wvBmSRRQlZld-luauRenGua2DpxqBscI0KuD5ACsN6Y9BAcm3-ZXYx"
#     client_ID = "NVFow3aK-2RZfpXZSc2-Ng"
#     headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
#     parameters = {"term": "restaurants",
#                 "limit": 50,
#                 "offset": 150,
#                 "location": "Austin"}

#     # get the requests 
#     response = requests.get(url, headers = headers, params = parameters) 

#     # print the text from the response object 
#     if response.status_code == 200: 
        
#         # returns a data 
#         data = json.loads(response.text)
#         with open("yelp_menus4.json", "w") as fp:
#             json.dump(data , fp, indent = 4) 

#     #### MENU ITEMS API CALL #### 

#     url = "https://edamam-recipe-search.p.rapidapi.com/api/recipes/v2"

#     cuisines = ["Nordic", "Central europe", "South american", "American", "French", "Italian", "Middle eastern", "Eastern europe",
#                 "Asian", "Mexican", "South east asian", "Indian", "Mediterranean", "Kosher", "British", "Chinese", "Japanese"]

#     for i in range(len(cuisines)): 
#         querystring = {"type":"public","co2EmissionsClass":"A","beta":"false","random":"true","cuisineType[0]": cuisines[i],"imageSize[0]":"LARGE"}

#         headers = {
#             "Accept-Language": "en",
#             "X-RapidAPI-Key": "dd7a6afc1amshacd315e470612c6p1565e5jsnac4a58de874e",
#             "X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com"
#         }

#         response = requests.get(url, headers=headers, params=querystring)

#         if response.status_code == 200: 
            
#             # returns a data 
#             data = json.loads(response.text)

#             filename = f'recipes{i + 1}.json'
#             with open(filename, "w") as fp:
#                 json.dump(data , fp, indent = 4) 

''' CLEAN DATA GATHERED SO FAR '''
# def menus_and_rests(): 
#     ###### CREATE DICTIONARY OF AUSTIN RESTAURANTS #######
#     restaurants = {} 
#     restaurants["restaurants"] = []
#     north = [78727, 78728, 78753, 78758]
#     south = [78652, 78745, 78748]
#     west = [78730, 78732]
#     east = [78702, 78722, 78723, 78724]
#     central = [78701, 78702, 78703, 78704, 78705, 78712, 78722, 78731, 78741, 78746, 78751, 78752, 78756, 78757]

#     id = -1 

#     # iterate through all of the json files 
#     for i in range(1, 6):
#         filename = f'yelp_menus{i}.json'
#         file = open(filename)
#         yelp_dict = json.load(file)
        

#         # iterate through the response dictionary and select the data we want 
#         for business in yelp_dict["businesses"]:
#             id += 1 
#             restaurants["restaurants"].append({})

#             # unique ID for restaurant
#             restaurants["restaurants"][id]["id"] = id        

#             # get the restaurant's name 
#             restaurants["restaurants"][id]["name"] = business["name"]

#             # get the restaurant's image URL 
#             restaurants["restaurants"][id]["image"] = business["image_url"]

#             # get the restaurant's rating 
#             restaurants["restaurants"][id]["rating"] = business["rating"]

#             # get the restaurant's tags 
#             restaurants["restaurants"][id]["tags"] = [] 
#             for category in business["categories"]:
#                 asian = ["Chinese", "Japanese", "Korean", "Vietnamese", "Filipino", "Thai", "Asian Fusion", "Cantonese", "Dim Sum", "Polynesian"]
#                 southeast_asian = ["Vietnamese", "Filipino", "Thai"]
#                 nordic = ["Denmark", "Finland", "Iceland", "Norway", "Sweden"] 

#                 if (category["title"] in southeast_asian) and ("South east asian" not in restaurants["restaurants"][id]["tags"]): 
#                     restaurants["restaurants"][id]["tags"].append("South east asian")
#                 elif category["title"] in asian and ("Asian" not in restaurants["restaurants"][id]["tags"]): 
#                     restaurants["restaurants"][id]["tags"].append("Asian")
#                 elif category["title"] in nordic and ("Nordic" not in restaurants["restaurants"][id]["tags"]): 
#                     restaurants["restaurants"][id]["tags"].append("Nordic") 

#                 if (category["title"] not in restaurants["restaurants"][id]["tags"]):
#                     restaurants["restaurants"][id]["tags"].append(category["title"])

#             # get the restaurant's phone 
#             restaurants["restaurants"][id]["phone"] = business["display_phone"]

#             # get and determine the region of Austin 
#             if int(business["location"]["zip_code"]) in north: 
#                 restaurants["restaurants"][id]["location"] = "North Austin"
#             elif int(business["location"]["zip_code"]) in south: 
#                 restaurants["restaurants"][id]["location"] = "South Austin"
#             elif int(business["location"]["zip_code"]) in east: 
#                 restaurants["restaurants"][id]["location"] = "East Austin"
#             elif int(business["location"]["zip_code"]) in west: 
#                 restaurants["restaurants"][id]["location"] = "West Austin"
#             else:
#                 restaurants["restaurants"][id]["location"] = "Central Austin"

#     # save restaurants to a json file for now 
#     with open("restaurants.json", "w") as fp:
#         json.dump(restaurants , fp, indent = 4)  

#     ########### CLEAN THE DATA ##############

#     menu_items = {} 
#     menu_items["menu_items"] = []

#     id = -1 

#     for i in range (1, 6): 
#         # iterate through all of the json files 
#         filename = f'recipes{i}.json'
#         file = open(filename)
#         init_menu_dict = json.load(file)
#         menu_dict = init_menu_dict["hits"]

#         # iterate through the response dictionary and select the data we want 
#         for recipe in menu_dict:
#             # since the requests are randomized, there is a possibility that the API returned the same menu item twice during different calls 
#             if recipe["recipe"]["label"] in menu_items["menu_items"]:
#                 continue 

#             id += 1 

#             menu_items["menu_items"].append({})

#             # unique ID for the menu item
#             menu_items["menu_items"][id]["id"] = id        

#             # get the image for the menu item 
#             menu_items["menu_items"][id]["image"] = recipe["recipe"]["images"]["SMALL"]["url"]

#             # get the name of the menu item and normalize it 
#             name = recipe["recipe"]["label"]
#             name = name.lower()
#             name = name.capitalize()
#             menu_items["menu_items"][id]["name"] = name

#             # get the dietary labels for the menu item 
#             menu_items["menu_items"][id]["dietary"] = recipe["recipe"]["healthLabels"]

#             # get the list of ingredients for the menu item 
#             menu_items["menu_items"][id]["ingredients"] = recipe["recipe"]["ingredientLines"]

#             # get the nutrition facts for the menu item (calories and macros) 
#             nutrition = {
#                 "Calories": f'{int(recipe["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"])} kcal',
#                 "Carbs": f'{recipe["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]: .1f} g of carbs',
#                 "Protein": f'{recipe["recipe"]["totalNutrients"]["PROCNT"]["quantity"]: .1f} g of protein',
#                 "Fat": f'{recipe["recipe"]["totalNutrients"]["FAT"]["quantity"]: .1f} g of fat' 
#             } 

#             # put calories as a separate attribute for now 
#             menu_items["menu_items"][id]["nutrition"] = nutrition
#             menu_items["menu_items"][id]["calories"] = int(recipe["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"])
            
#             # get the cuisine type for the menu item 
#             cuisines = recipe["recipe"]["cuisineType"]
#             for i in range(len(cuisines)):  
#                 cuisines[i] = cuisines[i].capitalize()

#             menu_items["menu_items"][id]["cuisine"] = cuisines

#     # get the list of restaurants 
#     restaurant_list = restaurants["restaurants"]

#     asian = ["Chinese", "Japanese", "Korean", "Vietnamese", "Filipino", "Thai", "Asian Fusion", "Cantonese", "Dim Sum", "Polynesian"]
#     southeast_asian = ["Vietnamese", "Filipino", "Thai"]
#     nordic = ["Denmark", "Finland", "Iceland", "Norway", "Sweden"] 

#     for menu_item in menu_items["menu_items"]: 
#         menu_item["restaurants"] = {} 
#         menu_item["restaurant_id"] = {}

#         for cuisine in menu_item["cuisine"]: 
#             menu_item["restaurants"][cuisine] = []
#             menu_item["restaurant_id"][cuisine] = []
        
#         # look through the list of restaurants
#         for restaurants in restaurant_list: 
                
#             # look through the tags of a restaurant
#             for tag in restaurants["tags"]:

#                 # only proceed if restaurant hasn't been added 
#                 if restaurants["name"] not in menu_item["restaurants"]:
#                     temp_tag = tag 
#                     if tag == "New American" or tag == "Southern":
#                         temp_tag = "American"
#                     elif tag == "Latin American" or tag == "Peruvian": 
#                         temp_tag = "South american"

#                     # check if the cuisine from menu item is too general 
#                     for cuisine in menu_item["cuisine"]: 

#                         if cuisine == "Asian": 
#                             if temp_tag in asian: 
#                                 menu_item["restaurants"][cuisine].append(restaurants["name"])
#                                 menu_item["restaurant_id"][cuisine].append(restaurants["id"])
#                                 break

#                         elif cuisine == "South east asian": 
#                             if temp_tag in southeast_asian: 
#                                 menu_item["restaurants"][cuisine].append(restaurants["name"])
#                                 menu_item["restaurant_id"][cuisine].append(restaurants["id"])
#                                 break

#                         elif cuisine == "Nordic":
#                             if temp_tag in nordic:
#                                 menu_item["restaurants"][cuisine].append(restaurants["name"])
#                                 menu_item["restaurant_id"][cuisine].append(restaurants["id"])
#                                 break

#                         elif temp_tag in menu_item["cuisine"]:
#                             menu_item["restaurants"][cuisine].append(restaurants["name"])
#                             menu_item["restaurant_id"][cuisine].append(restaurants["id"])
#                             break

#     # save menu items to a json file 
#     with open("menu_items.json", "w") as fp:
#         json.dump(menu_items , fp, indent = 4)

''' OBTAIN DATA FROM LAST API '''
# def clean_cuisines(): 
#     ##### DETERMINE THE POSSIBLE CUISINES NEEDED ##### 
#     filename = "menu_items.json"
#     file = open(filename)
#     menu_items = json.load(file)

#     # find out which cuisines/countries we need to gather data from APIs 
#     cuisines = []

#     # iterate through the menu items and add any new cuisine to the "cuisines"
#     for menu_item in menu_items["menu_items"]: 
#         for item in menu_item["cuisine"]: 
#             if item not in cuisines: 
#                 cuisines.append(item)

#     '''
#     CUISINES = ['Nordic', 
#                 'Central europe', 
#                 'South american', 
#                 'American',
#                 'French', 
#                 'Italian', 
#                 'Middle eastern', 
#                 'Eastern europe', 
#                 'Asian', 
#                 'Mexican', 
#                 'South east asian', 
#                 'Indian', 
#                 'Mediterranean', 
#                 'Kosher', 
#                 'British', 
#                 'Chinese']
#     '''

#     ### Since there are considerably less cuisines than the other models, we can keep the subregion as cuisines, but 
#     ### predefine some of the countries that make up the subregion and use those predefined regions to go to an API 
#     ### that specializes in country data and grab the flag information for all of the countries. 

#     cuisine_model = {}
#     cuisine_model["cuisines"] = []
#     id = -1

#     # iterate through CUISINES list and add each entry into the dictionary 
#     for cuisine in cuisines: 
#         cuisine_model["cuisines"].append({})

#         # create a unique ID for each cuisine 
#         id += 1 
#         cuisine_model["cuisines"][id]["id"] = id 
        
#         # set the name for the cuisine 
#         cuisine_model["cuisines"][id]["name"] = cuisine 

#         # create an empty list for menu items 
#         cuisine_model["cuisines"][id]["menu_items"] = [] 

#         # create an empty list for the unique id for menu items
#         cuisine_model["cuisines"][id]["menu_id"] = []

#         # create an empty list for restaurants 
#         cuisine_model["cuisines"][id]["restaurants"] = [] 

#         # create an empty list for the unique id for restaurants
#         cuisine_model["cuisines"][id]["restaurant_id"] = []

#     # make sure Asian cuisine is included 

#     # go through the list of menu items available and determine which are part of which cuisine
#     for menu_item in menu_items["menu_items"]: 

#         for cuisine in cuisine_model["cuisines"]: 

#             # the menu item is a part of a certain cuisine 
#             for tag in menu_item["cuisine"]: 

#                 # haven't added the menu item to the cuisine yet and matches
#                 if tag == cuisine["name"] and menu_item["name"] not in cuisine["menu_items"] : 
#                     cuisine["menu_items"].append(menu_item["name"])
#                     cuisine["menu_id"].append(menu_item["id"])

#                     # also add all current restaurants into the restaurants attribute if they're not there yet 
#                     for index in range(len(menu_item["restaurants"][cuisine["name"]])):
#                         # restaurant isn't in cuisine yet 
#                         if menu_item["restaurants"][cuisine["name"]][index] not in cuisine["restaurants"]:
#                             cuisine["restaurants"].append(menu_item["restaurants"][cuisine["name"]][index])
#                             cuisine["restaurant_id"].append(menu_item["restaurant_id"][cuisine["name"]][index])

#     # determine the countries and flags for each subregion cuisine 
#     subregions = ["Central europe", "South america", "Eastern europe", "Asia", "South-eastern asia" ]

#     for subregion in subregions: 

#         # call API for subregion 
#         url = f"https://restcountries.com/v3.1/region/{subregion}"

#         response = requests.get(url)

#         if response.status_code == 200: 
#             # returns a data 
#             data = json.loads(response.text)
#             with open(f"{subregion}.json", "w") as fp:
#                 json.dump(data , fp, indent = 4) 


#         # open the newly made file and read the data inside and add to where relevant in current cuisine dict 
#         filename = f'{subregion}.json'
#         file = open(filename) 
#         current = json.load(file)

#         for cuisine in cuisine_model["cuisines"]: 
#             if cuisine["name"][:len(subregion)] == subregion or cuisine["name"] == "South east asian": 
#                 cuisine["countries"] = [] 
#                 cuisine["flags"] = [] 
#                 for i in range(len(current)): 
#                     cuisine["countries"].append(current[i]["name"]["common"])
#                     cuisine["flags"].append(current[i]["flags"]["png"])

#     # # determine the country and flag for each singular-country cuisine 
#     remaining = {
#         "Nordic": ["Denmark", "Finland", "Iceland", "Norway"],
#         "American": ["United States"],
#         "French": ["France"],
#         "Italian": ["Italy"],
#         "Mexican": ["Mexico"],
#         "Indian": ["India"],
#         "Kosher": ["Israel"],
#         "British": ["United Kingdom"],
#         "Chinese": ["China"],
#         "Middle eastern": ["Iraq", "Yemen", "UAE", "Kuwait"],
#         "Mediterranean": ["Greece", "Italy", "Spain", "Morocco","Egypt", "Lebanon"],
#         "Japanese": ["Japan"],
#         "Korean": ["South Korea"],
#         "Caribbean": ["Antigua", "Bahamas", "Barbados", "Cuba", "Dominica", "Dominican Republic", "Grenada", "Haiti", "Jamaica", "Saint Lucia", "Saint Kitts", "Saint Vincent", "Trinidad"] 
#     }

#     for countries in remaining: 
#         for cuisine in cuisine_model["cuisines"]: 
#             # current cuisine 
#             if cuisine["name"] == countries: 
#                 cuisine["countries"] = []
#                 cuisine["flags"] = [] 


#                 for country in remaining[countries]: 
#                     url = f"https://restcountries.com/v3.1/name/{country}"

#                     response = requests.get(url)

#                     if response.status_code == 200: 
#                         # returns a data 
#                         current = response.json()

#                     else: 
#                         print(f'Error: {response.status_code}')


#                     for area in current: 

#                         if area["name"]["common"] == country:
#                             cuisine["countries"].append(country)
#                             cuisine["flags"].append(area["flags"]["png"])


#     #pprint.pprint(cuisine_model)
#     with open("cuisines.json", "w") as fp:
#         json.dump(cuisine_model , fp, indent = 4)

# def obtain_ids(): 
#     # load all of the necessary files 
#     filename1 = f'restaurants.json'
#     file1 = open(filename1)
#     restaurant = json.load(file1)
#     restaurants = restaurant["restaurants"]

#     filename2 = f'menu_items.json'
#     file2 = open(filename2)
#     menu_items_list = json.load(file2)
#     menu_items = menu_items_list["menu_items"]

#     filename3 = f'cuisines.json'
#     file3 = open(filename3)
#     cuisine_list = json.load(file3)
#     cuisines = cuisine_list["cuisines"]

#     # obtain IDs of cuisines for menu items 
#     # look through every menu item and assign unique ID of cuisines
#     for menu_item in menu_items: 
#         menu_item["cuisine_id"] = [] 

#         for tags in menu_item["cuisine"]: 
#             for cuisine in cuisines: 
#                 if tags == cuisine["name"]:
#                     menu_item["cuisine_id"].append(cuisine["id"])

#     # save restaurants to a json file 
#     with open("menu_items.json", "w") as fp:
#         json.dump(menu_items , fp, indent = 4)  

#     # obtain IDs of cuisines and menu items for restaurants
#     # iterate through the entire list of restaurants 
#     for restaurant in restaurants:
#         restaurant["menu_items_id"] = [] 
#         restaurant["menu_items"] = [] 

#         restaurant["cuisine_id"] = [] 

#         for cuisine in cuisines: 
#             # restaurant is a part of this cuisine 
#             if restaurant["id"] in cuisine["restaurant_id"]:
#                 restaurant["cuisine_id"].append(cuisine["id"])
                
#                 # all of the menu items in this cuisine will be linked to the restaurant 
#                 for index in range(len(cuisine["menu_items"])): 
#                     restaurant["menu_items_id"].append(cuisine["menu_id"][index])
#                     restaurant["menu_items"].append(cuisine["menu_items"][index])

#                 # make sure that the tag for the cuisine is the tag for restaurant id 
#                 if cuisine["name"] not in restaurant["tags"]: 
#                     restaurant["tags"].append(cuisine["name"])

#     # save restaurants to a json file 
#     with open("restaurants.json", "w") as fp:
#         json.dump(restaurants , fp, indent = 4) 

''' READ STATIC FILES FROM APIS AND POPULATE TABLES '''
def create_restaurant():
    """
    Populate the restaurant table with data from restaurants.json.
    """

    # load the cleaned data 
    restaurants = load_json('restaurants.json')

    for item in restaurants:
        # Assuming 'cuisine_ids' is an array of IDs in your JSON
        cuisine_instances = [Cuisine.query.get(cuisine_id) for cuisine_id in item['cuisine_id'] if Cuisine.query.get(cuisine_id)]
    
        newRestaurant = Restaurant(
            id=item["id"],
            name=item['name'],
            image=item['image'],
            location=item['location'],
            phone=item['phone'],
            tags = json.dumps(item.get('tags', [])),
            rating=item['rating'],
            cuisines=cuisine_instances  # Associate the restaurant with its cuisines through the association table.
        )
        db.session.add(newRestaurant)
    db.session.commit()

def create_cuisines():
    """
    Populate the cuisines table with data from cuisines.json.
    """
    cuisines = load_json('cuisines.json')['cuisines']

    for cuisine in cuisines:
        newCuisine = Cuisine(
            id=cuisine['id'],
            name=cuisine['name'],
            countries=json.dumps(cuisine.get('countries', [])),  # Storing as JSON string
            flags=json.dumps(cuisine.get('flags', []))  # Storing as JSON string
        )
        db.session.add(newCuisine)
    db.session.commit()

def create_menuitem():
    menu_items = load_json('menu_items.json')

    for item in menu_items:
        # Assuming 'cuisine_ids' is an array of IDs in your JSON
        cuisine_instances = [Cuisine.query.get(cuisine_id) for cuisine_id in item['cuisine_id'] if Cuisine.query.get(cuisine_id)]

        newMenuItem = MenuItem(
            id=item["id"],
            name=item['name'],
            ingredients=json.dumps(item.get('ingredients', [])),
            calories=item.get("calories", 500),
            dietary=json.dumps(item.get('dietary', [])),
            image=item['image'],
            cuisines=cuisine_instances, # Associate the menu item with its cuisines through the association table.
        )
        db.session.add(newMenuItem)
    db.session.commit()

def associate_restaurants_cuisines():
    restaurant_datas = load_json('restaurants.json')
    for restaurant_data in restaurant_datas:
        restaurant = Restaurant.query.get(restaurant_data['id'])
        if restaurant is None:
            print(f"Restaurant not found: {restaurant_data['id']}")
            continue  # Skip this restaurant if not found

        for cuisine_id in restaurant_data['cuisine_id']:
            cuisine = Cuisine.query.get(cuisine_id)
            if cuisine is None:
                print(f"Cuisine not found: {cuisine_id}")
                continue  # Skip this cuisine if not found

            insert_stmt = restaurant_cuisine.insert().values(restaurant_id=restaurant.id, cuisine_id=cuisine.id)
            db.session.execute(insert_stmt)

        db.session.commit()

def associate_menuitems_cuisines():
    menu_item_datas = load_json('menu_items.json')
    for menu_item_data in menu_item_datas:
        menu_item = MenuItem.query.get(menu_item_data['id'])
        if menu_item is None:
            print(f"Restaurant not found: {menu_item_data['id']}")
            continue  # Skip this restaurant if not found

        for cuisine_id in menu_item_data['cuisine_id']:
            cuisine = Cuisine.query.get(cuisine_id)
            if cuisine is None:
                print(f"Cuisine not found: {cuisine_id}")
                continue  # Skip this cuisine if not found

            insert_stmt = menu_item_cuisine.insert().values(menu_item_id=menu_item.id, cuisine_id=cuisine.id)
            db.session.execute(insert_stmt)

        db.session.commit()


def setup_database():
    # Wrap the database setup and population in a function
    db.drop_all()
    db.create_all()
    # call_apis()
    # menus_and_rests()
    # clean_cuisines()
    # obtain_ids()
    create_restaurant()
    create_menuitem()
    create_cuisines()
    associate_restaurants_cuisines()
    associate_menuitems_cuisines()

setup_database()
