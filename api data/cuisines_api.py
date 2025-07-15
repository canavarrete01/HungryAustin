import requests 
import json
import pprint

##### DETERMINE THE POSSIBLE CUISINES NEEDED ##### 
filename = "menu_items.json"
file = open(filename)
menu_items = json.load(file)

# find out which cuisines/countries we need to gather data from APIs 
cuisines = []

# iterate through the menu items and add any new cuisine to the "cuisines"
for menu_item in menu_items["menu_items"]: 
    for item in menu_item["cuisine"]: 
        if item not in cuisines: 
            cuisines.append(item)

'''
CUISINES = ['Nordic', 
            'Central europe', 
            'South american', 
            'American',
            'French', 
            'Italian', 
            'Middle eastern', 
            'Eastern europe', 
            'Asian', 
            'Mexican', 
            'South east asian', 
            'Indian', 
            'Mediterranean', 
            'Kosher', 
            'British', 
            'Chinese']
'''

### Since there are considerably less cuisines than the other models, we can keep the subregion as cuisines, but 
### predefine some of the countries that make up the subregion and use those predefined regions to go to an API 
### that specializes in country data and grab the flag information for all of the countries. 

cuisine_model = {}
cuisine_model["cuisines"] = []
id = -1

# iterate through CUISINES list and add each entry into the dictionary 
for cuisine in cuisines: 
    cuisine_model["cuisines"].append({})

    # create a unique ID for each cuisine 
    id += 1 
    cuisine_model["cuisines"][id]["id"] = id 
    
    # set the name for the cuisine 
    cuisine_model["cuisines"][id]["name"] = cuisine 

    # create an empty list for menu items 
    cuisine_model["cuisines"][id]["menu_items"] = [] 

    # create an empty list for the unique id for menu items
    cuisine_model["cuisines"][id]["menu_id"] = []

    # create an empty list for restaurants 
    cuisine_model["cuisines"][id]["restaurants"] = [] 

    # create an empty list for the unique id for restaurants
    cuisine_model["cuisines"][id]["restaurant_id"] = []


# pprint.pprint(cuisine_model)

# go through the list of menu items available and determine which are part of which cuisine
for menu_item in menu_items["menu_items"]: 


    for cuisine in cuisine_model["cuisines"]: 

        # the menu item is a part of a certain cuisine 
        for tag in menu_item["cuisine"]: 

            # haven't added the menu item to the cuisine yet and matches
            if tag == cuisine["name"] and menu_item["name"] not in cuisine["menu_items"] : 
                cuisine["menu_items"].append(menu_item["name"])
                cuisine["menu_id"].append(menu_item["id"])

                # also add all current restaurants into the restaurants attribute if they're not there yet 
                for index in range(len(menu_item["restaurants"][cuisine["name"]])):
                    # restaurant isn't in cuisine yet 
                    if menu_item["restaurants"][cuisine["name"]][index] not in cuisine["restaurants"]:
                        cuisine["restaurants"].append(menu_item["restaurants"][cuisine["name"]][index])
                        cuisine["restaurant_id"].append(menu_item["restaurant_id"][cuisine["name"]][index])

# determine the countries and flags for each subregion cuisine 
subregions = ["Central europe", "South america", "Eastern europe", "Asia", "South-eastern asia" ]

for subregion in subregions: 

    # call API for subregion 
    # url = f"https://restcountries.com/v3.1/region/{subregion}"

    # response = requests.get(url)

    # if response.status_code == 200: 
    #     # returns a data 
    #     data = json.loads(response.text)
    #     with open(f"{subregion}.json", "w") as fp:
    #         json.dump(data , fp, indent = 4) 

    # else: 
    #     print(f'Error: {response.status_code}')

    # open the newly made file and read the data inside and add to where relevant in current cuisine dict 
    filename = f'{subregion}.json'
    file = open(filename) 
    current = json.load(file)

    for cuisine in cuisine_model["cuisines"]: 
        if cuisine["name"][:len(subregion)] == subregion or cuisine["name"] == "Southeast asian": 
            cuisine["countries"] = [] 
            cuisine["flags"] = [] 
            for i in range(len(current)): 
                cuisine["countries"].append(current[i]["name"]["common"])
                cuisine["flags"].append(current[i]["flags"]["png"])

# # determine the country and flag for each singular-country cuisine 
remaining = {
    "Nordic": ["Denmark", "Finland", "Iceland", "Norway"],
    "American": ["United States"],
    "French": ["France"],
    "Italian": ["Italy"],
    "Mexican": ["Mexico"],
    "Indian": ["India"],
    "Kosher": ["Israel"],
    "British": ["United Kingdom"],
    "Chinese": ["China"],
    "Middle eastern": ["Iraq", "Yemen", "UAE", "Kuwait"],
    "Mediterranean": ["Greece", "Italy", "Spain", "Morocco","Egypt", "Lebanon"] 
}
for countries in remaining: 
    for cuisine in cuisine_model["cuisines"]: 
        # current cuisine 
        if cuisine["name"] == countries: 
            cuisine["countries"] = []
            cuisine["flags"] = [] 


            for country in remaining[countries]: 
                url = f"https://restcountries.com/v3.1/name/{country}"

                response = requests.get(url)

                if response.status_code == 200: 
                    # returns a data 
                    current = response.json()

                else: 
                    print(f'Error: {response.status_code}')


                for area in current: 

                    if area["name"]["common"] == country:
                        cuisine["countries"].append(country)
                        cuisine["flags"].append(area["flags"]["png"])


#pprint.pprint(cuisine_model)
with open("cuisines.json", "w") as fp:
    json.dump(cuisine_model , fp, indent = 4)