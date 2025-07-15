import requests
import json
import pprint

########### OBTAIN THE DATA ############# 
'''
url = "https://edamam-recipe-search.p.rapidapi.com/api/recipes/v2"

cuisines = ["Italian", "Chinese", "Korean", "Mexican", "American"]

    for i in range(len(cuisines): 
    querystring = {"type":"public","co2EmissionsClass":"A","beta":"false","random":"true","cuisineType[0]": cuisine[i],"imageSize[0]":"LARGE"}

    headers = {
        "Accept-Language": "en",
        "X-RapidAPI-Key": "dd7a6afc1amshacd315e470612c6p1565e5jsnac4a58de874e",
        "X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200: 
        
        # returns a data 
        data = json.loads(response.text)
        pprint.pprint(data)

        filename = f'recipes{i + 1}.json'
        with open(filename, "w") as fp:
            json.dump(data , fp, indent = 4) 

    else: 
        print(f'Error: {response.status_code}')
'''

########### CLEAN THE DATA ##############

menu_items = {} 
menu_items["menu_items"] = []

id = -1 

for i in range (1, 6): 
    # iterate through all of the json files 
    filename = f'recipes{i}.json'
    file = open(filename)
    init_menu_dict = json.load(file)
    menu_dict = init_menu_dict["hits"]

    # iterate through the response dictionary and select the data we want 
    for recipe in menu_dict:
        # since the requests are randomized, there is a possibility that the API returned the same menu item twice during different calls 
        if recipe["recipe"]["label"] in menu_items["menu_items"]:
            continue 

        id += 1 

        menu_items["menu_items"].append({})

        # unique ID for the menu item
        menu_items["menu_items"][id]["id"] = id        

        # get the image for the menu item 
        menu_items["menu_items"][id]["image"] = recipe["recipe"]["images"]["SMALL"]["url"]

        # get the name of the menu item 
        menu_items["menu_items"][id]["name"] = recipe["recipe"]["label"]

        # get the dietary labels for the menu item 
        menu_items["menu_items"][id]["dietary"] = recipe["recipe"]["healthLabels"]

        # get the list of ingredients for the menu item 
        menu_items["menu_items"][id]["ingredients"] = recipe["recipe"]["ingredientLines"]

        # get the nutrition facts for the menu item (calories and macros) 
        nutrition = {
            "Calories": f'{int(recipe["recipe"]["totalNutrients"]["ENERC_KCAL"]["quantity"])} kcal',
            "Carbs": f'{recipe["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]: .1f} g of carbs',
            "Protein": f'{recipe["recipe"]["totalNutrients"]["PROCNT"]["quantity"]: .1f} g of protein',
            "Fat": f'{recipe["recipe"]["totalNutrients"]["FAT"]["quantity"]: .1f} g of fat' 
        } 

        menu_items["menu_items"][id]["nutrition"] = nutrition

        # get the cuisine type for the menu item 
        cuisines = recipe["recipe"]["cuisineType"]
        for i in range(len(cuisines)):  
            cuisines[i] = cuisines[i].capitalize()

        menu_items["menu_items"][id]["cuisine"] = cuisines


# open the file for restaurants and add restaurants of the same cuisine to the menu item 
filename2 = f'restaurants.json'
file2 = open(filename2)
restaurant = json.load(file2)
restaurant_list = restaurant["restaurants"]

asian = ["Chinese", "Japanese", "Korean", "Vietnamese", "Filipino", "Thai", "Asian Fusion", "Cantonese", "Dim Sum", "Polynesian"]
southeast_asian = ["Vietnamese", "Filipino", "Thai"]
nordic = ["Denmark", "Finland", "Iceland", "Norway", "Sweden"] 

for menu_item in menu_items["menu_items"]: 
    menu_item["restaurants"] = {} 
    menu_item["restaurant_id"] = {}

    for cuisine in menu_item["cuisine"]: 
        menu_item["restaurants"][cuisine] = []
        menu_item["restaurant_id"][cuisine] = []
    # look through the list of restaurants
    for restaurants in restaurant_list: 
            
            # look through the tags of a restaurant
            for tag in restaurants["tags"]:

                # only proceed if restaurant hasn't been added 
                if restaurants["name"] not in menu_item["restaurants"]:
                    temp_tag = tag 
                    if tag == "New American" or tag == "Southern":
                        temp_tag = "American"
                    elif tag == "Latin American" or tag == "Peruvian": 
                        temp_tag = "South american"

                    # check if the cuisine from menu item is too general 
                    for cuisine in menu_item["cuisine"]: 

                        if cuisine == "Asian": 
                            if temp_tag in asian: 
                                menu_item["restaurants"][cuisine].append(restaurants["name"])
                                menu_item["restaurant_id"][cuisine].append(restaurants["id"])
                                break

                        elif cuisine == "South east asian": 
                            if temp_tag in southeast_asian: 
                                menu_item["restaurants"][cuisine].append(restaurants["name"])
                                menu_item["restaurant_id"][cuisine].append(restaurants["id"])
                                break

                        elif cuisine == "Nordic":
                            if temp_tag in nordic:
                                menu_item["restaurants"][cuisine].append(restaurants["name"])
                                menu_item["restaurant_id"][cuisine].append(restaurants["id"])
                                break

                        elif temp_tag in menu_item["cuisine"]:
                            menu_item["restaurants"][cuisine].append(restaurants["name"])
                            menu_item["restaurant_id"][cuisine].append(restaurants["id"])
                            break

# add cuisine ID to each menu item 
filename3 = f'cuisines.json'
file3 = open(filename3)
cuisine_list = json.load(file3)
cuisines = cuisine_list["cuisines"]

# look through every menu item and assign unique ID of cuisines
for menu_item in menu_items["menu_items"]: 
    menu_item["cuisine_id"] = [] 

    for tags in menu_item["cuisine"]: 
        for cuisine in cuisines: 
            if tags == cuisine["name"]:
                menu_item["cuisine_id"].append(cuisine["id"])


# save restaurants to a json file 
with open("menu_items.json", "w") as fp:
    json.dump(menu_items , fp, indent = 4) 
