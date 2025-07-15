from flask import Flask, jsonify, abort, request, render_template
import json
import requests
import re
from Create_db import app, db, Cuisine, Restaurant, MenuItem, setup_database 
import subprocess

url = "http://localhost:5000"
headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}


@app.route('/')
@app.route('/home/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/restaurant/')
def restaurant():
    query = request.args.get('query')
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')
    
    global url 
    global headers

    if query: 
        query = query.strip()
        response = requests.get(f'{url}/api/v1/restaurants/search?query={query}', headers=headers)

    elif sort_by and sort_order:
        response = requests.get(f'{url}/api/v1/restaurants/sort?&sort_by={sort_by}&sort_order={sort_order}', headers=headers)
    
    else:
        response = requests.get(f'{url}/api/v1/restaurants/', headers=headers)

    restaurants = response.json()["restaurants"]
    return render_template("restaurant.html", restaurants=restaurants)



@app.route('/restaurant/<int:id>')
def restaurant_menu(id):

    global url
    global headers

    response = requests.get(f'{url}/api/v1/restaurants/{id}', headers=headers)
    restaurant = response.json()['restaurant']

    response = requests.get(f'{url}/api/v1/menu_items/', headers=headers)
    menu_item = response.json()["menu_items"]

    response = requests.get(f'{url}/api/v1/cuisines/', headers=headers)
    cuisines = response.json()["cuisines"]

    return render_template("menu.html", restaurant=restaurant, menu_items=menu_item, cuisines=cuisines)


@app.route('/cuisines/')
def cuisines():
    query = request.args.get("query")
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')
    
    global url
    global headers

    if query:
        query = query.strip()
        response = requests.get(f'{url}/api/v1/cuisines/search?query={query}', headers=headers)
    elif sort_by and sort_order:
        response = requests.get(f'{url}/api/v1/cuisines/sort?&sort_by={sort_by}&sort_order={sort_order}')
    
    else: 
        response = requests.get(f'{url}/api/v1/cuisines/')

    cuisines = response.json()['cuisines']
    return render_template("cuisines.html", cuisines=cuisines)

@app.route('/cuisines/<int:id>')
def cuisine_menu(id):

    global url
    global headers

    response = requests.get(f'{url}/api/v1/cuisines/{id}', headers=headers)
    cuisine = response.json()['cuisine']
    
    response = requests.get(f'{url}/api/v1/restaurants/', headers=headers)
    restaurant = response.json()["restaurants"]

    response = requests.get(f'{url}/api/v1/menu_items/', headers=headers)
    menu_item = response.json()["menu_items"]

    return render_template("cuisine_menu.html", cuisine=cuisine, restaurants=restaurant, menu_items=menu_item)

@app.route('/dishes/')
def dishes():

    global url
    global headers

    query = request.args.get('query')
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    if query: 
        query = query.strip() 
        response = requests.get(f'{url}/api/v1/menu_items/search?query={query}', headers=headers)

    elif sort_by and sort_order: 
        response = requests.get(f'{url}/api/v1/menu_items/sort?sort_by={sort_by}&sort_order={sort_order}', headers=headers)
    
    else:        
        response = requests.get(f'{url}/api/v1/menu_items/', headers=headers)


    # get all instances of cuisines and restaurant
    cuisines_response = requests.get(f'{url}/api/v1/cuisines/', headers=headers)
    cuisines = cuisines_response.json()['cuisines']

    restaurant_response = requests.get(f'{url}/api/v1/restaurants/', headers=headers)
    restaurant = restaurant_response.json()['restaurants']

    
    menu_items = response.json()['menu_items']
    return render_template("dishes.html", menu_items=menu_items, cuisines=cuisines, restaurant=restaurant)

@app.route('/dishes/<int:id>')
def dish_details(id):

    global url
    global headers

    response = requests.get(f'{url}/api/v1/menu_items/{id}', headers=headers)
    dish = response.json()['menu_item']

    response  = requests.get(f'{url}/api/v1/cuisines/', headers=headers)
    cuisines = response.json()["cuisines"]

    response = requests.get(f'{url}/api/v1/restaurants/', headers=headers)
    restaurant = response.json()["restaurants"]

    return render_template("dish_restaurants.html", dish=dish, cuisines=cuisines, restaurants=restaurant)

#### API IMPLEMENTATION #### 

# GET a list of all of the restaurants in default order 
@app.route('/api/v1/restaurants/', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.order_by(Restaurant.id.asc())
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'image': restaurant.image,
            'location': restaurant.location,
            'phone': restaurant.phone,
            'tags': json.loads(restaurant.tags),
            'rating': restaurant.rating,
            'cuisines': [cuisine.id for cuisine in restaurant.cuisines]
        }

        restaurant_list.append(restaurant_data)

    return jsonify({'restaurants': restaurant_list})


# GET a single restaurant
@app.route('/api/v1/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        abort(404)
    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'image': restaurant.image,
        'location': restaurant.location,
        'phone': restaurant.phone,
        'tags': json.loads(restaurant.tags),
        'rating': restaurant.rating,
        'cuisines': [cuisine.id for cuisine in restaurant.cuisines]
    }
    return jsonify({'restaurant': restaurant_data})

# GET all of the cuisines in default order 
@app.route('/api/v1/cuisines/', methods=['GET'])
def get_cuisines():
    cuisines = Cuisine.query.order_by(Cuisine.id.asc())
    cuisine_list = []
    for cuisine in cuisines:
        cuisine_data = {
            'id': cuisine.id,
            'name': cuisine.name,
            'countries': json.loads(cuisine.countries),
            'flags': json.loads(cuisine.flags),
            'restaurants': [restaurant.id for restaurant in cuisine.restaurants],
            'menu_items': [menu_item.id for menu_item in cuisine.menu_items]
        }

        cuisine_list.append(cuisine_data)
    return jsonify({'cuisines': cuisine_list})

# GET a single cuisine 
@app.route('/api/v1/cuisines/<int:cuisine_id>', methods=['GET'])
def get_cuisine(cuisine_id):
    cuisine = Cuisine.query.get(cuisine_id)
    if not cuisine:
        abort(404)
    cuisine_data = {
        'id': cuisine.id,
        'name': cuisine.name,
        'countries': json.loads(cuisine.countries),
        'flags': json.loads(cuisine.flags),
        'restaurants': [restaurant.id for restaurant in cuisine.restaurants],
        'menu_items': [menu_item.id for menu_item in cuisine.menu_items]
    }
    return jsonify({'cuisine': cuisine_data})

# GET all of the menu items in default order 
@app.route('/api/v1/menu_items/', methods=['GET'])
def get_menu_items():
    menu_items = MenuItem.query.order_by(MenuItem.id.asc())
    menu_item_list = []
    for menu_item in menu_items:
        menu_item_data = {
            'id': menu_item.id,
            'name': menu_item.name,
            'ingredients': json.loads(menu_item.ingredients),
            'calories': menu_item.calories,
            'dietary': json.loads(menu_item.dietary),
            'image': menu_item.image,
            'cuisines': [cuisine.id for cuisine in menu_item.cuisines]
        }
        menu_item_list.append(menu_item_data)
    return jsonify({'menu_items': menu_item_list})

# GET a single menu item 
@app.route('/api/v1/menu_items/<int:menu_item_id>', methods=['GET'])
def get_menu_item(menu_item_id):
    menu_item = MenuItem.query.get(menu_item_id)
    if not menu_item:
        abort(404)
    menu_item_data = {
        'id': menu_item.id,
        'name': menu_item.name,
        'ingredients': json.loads(menu_item.ingredients),
        'calories': menu_item.calories,
        'dietary': json.loads(menu_item.dietary),
        'image': menu_item.image,
        'cuisines': [cuisine.id for cuisine in menu_item.cuisines]
    }
    return jsonify({'menu_item': menu_item_data})

# GET a sorted list of restaurants 
@app.route('/api/v1/restaurants/sort', methods=['GET'])
def sort_restaurants():
    sort_by = request.args.get('sort_by', 'id')  # Default sort by ID
    sort_order = request.args.get('sort_order', 'asc')  # Default sort order is ascending

    if sort_by == 'name':
        restaurants = Restaurant.query.order_by(Restaurant.name.asc() if sort_order == 'asc' else Restaurant.name.desc())
    elif sort_by == 'rating':
        restaurants = Restaurant.query.order_by(Restaurant.rating.asc() if sort_order == 'asc' else Restaurant.rating.desc())
    else:
        restaurants = Restaurant.query.order_by(Restaurant.id.asc() if sort_order == 'asc' else Restaurant.id.desc())

    restaurant_list = []
    for restaurant in restaurants: 
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'image': restaurant.image,
            'location': restaurant.location,
            'phone': restaurant.phone,
            'tags': json.loads(restaurant.tags),
            'rating': restaurant.rating,
            'cuisines': [cuisine.name for cuisine in restaurant.cuisines]
        }

        restaurant_list.append(restaurant_data)
    
    return jsonify({'restaurants': restaurant_list})

# GET a sorted list of cuisines 
@app.route('/api/v1/cuisines/sort', methods=['GET'])
def sort_cuisines():
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    if sort_by == 'name':
        cuisines = Cuisine.query.order_by(Cuisine.name.asc() if sort_order == 'asc' else Cuisine.name.desc())
    else:
        cuisines = Cuisine.query.order_by(Cuisine.id.asc() if sort_order == 'asc' else Cuisine.id.desc())

    cuisine_list = []
    for cuisine in cuisines:
        cuisine_data = {
            'id': cuisine.id,
            'name': cuisine.name,
            'countries': json.loads(cuisine.countries),
            'flags': json.loads(cuisine.flags),
            'restaurants': [restaurant.name for restaurant in cuisine.restaurants],
            'menu_items': [menu_item.name for menu_item in cuisine.menu_items]
        }

        cuisine_list.append(cuisine_data)

    return jsonify({'cuisines': cuisine_list})

# GET a sorted list of menu items 
@app.route('/api/v1/menu_items/sort', methods=['GET'])
def sort_menu_items():
    sort_by = request.args.get('sort_by', 'id')
    sort_order = request.args.get('sort_order', 'asc')

    if sort_by == 'name':
        menu_items = MenuItem.query.order_by(MenuItem.name.asc() if sort_order == 'asc' else MenuItem.name.desc())
    elif sort_by == 'calories':
        menu_items = MenuItem.query.order_by(MenuItem.calories.asc() if sort_order == 'asc' else MenuItem.calories.desc())
    else:
        menu_items = MenuItem.query.order_by(MenuItem.id.asc() if sort_order == 'asc' else MenuItem.id.desc())

    menu_item_list = []
    for menu_item in menu_items:
        menu_item_data = {
            'id': menu_item.id,
            'name': menu_item.name,
            'ingredients': json.loads(menu_item.ingredients),
            'calories': menu_item.calories,
            'dietary': json.loads(menu_item.dietary),
            'image': menu_item.image,
            'cuisines': [cuisine.name for cuisine in menu_item.cuisines]
        }
        menu_item_list.append(menu_item_data)

    return jsonify({'menu_items': menu_item_list})

def highlight(text, search_term):  
    highlighted_text = re.sub(re.escape(search_term), f"<span style='background-color: yellow'>{search_term}</span>", text, flags=re.IGNORECASE)
    return highlighted_text


# GET a list of searched restaurants 
@app.route('/api/v1/restaurants/search', methods=["GET"])
def search_restaurants():
    query = request.args.get('query')

    restaurants = Restaurant.query.filter(Restaurant.name.ilike(f'%{query}%')).all()

    restaurant_list = []
    for restaurant in restaurants: 
        highlighted_name = highlight(restaurant.name, query)
        restaurant_data = {
            'id': restaurant.id,
            'name': highlighted_name,
            'image': restaurant.image,
            'location': restaurant.location,
            'phone': restaurant.phone,
            'tags': json.loads(restaurant.tags),
            'rating': restaurant.rating,
            'cuisines': [cuisine.name for cuisine in restaurant.cuisines]
        }

        restaurant_list.append(restaurant_data)
        
    return jsonify({'restaurants': restaurant_list})


# GET a list of searched cuisines 
@app.route('/api/v1/cuisines/search', methods=["GET"])
def search_cuisines(): 
    query = request.args.get("query")

    cuisines = Cuisine.query.filter(Cuisine.name.ilike(f'%{query}%')).all()
    cuisine_list = []
    for cuisine in cuisines:
        highlighted_name = highlight(cuisine.name, query)
        cuisine_data = {
            'id': cuisine.id,
            'name': highlighted_name,
            'countries': json.loads(cuisine.countries),
            'flags': json.loads(cuisine.flags),
            'restaurants': [restaurant.name for restaurant in cuisine.restaurants],
            'menu_items': [menu_item.name for menu_item in cuisine.menu_items]
        }
        cuisine_list.append(cuisine_data)
    return jsonify({'cuisines': cuisine_list})

# GET a list of searched menu items 
@app.route('/api/v1/menu_items/search', methods=["GET"])
def search_dishes():
    query = request.args.get("query")

    menu_items = MenuItem.query.filter(MenuItem.name.ilike(f'%{query}%')).all()
    menu_item_list = []
    for menu_item in menu_items:
        highlighted_name = highlight(menu_item.name, query)
        menu_item_data = {
            'id': menu_item.id,
            'name': highlighted_name,
            'ingredients': json.loads(menu_item.ingredients),
            'calories': menu_item.calories,
            'dietary': json.loads(menu_item.dietary),
            'image': menu_item.image,
            'cuisines': [cuisine.name for cuisine in menu_item.cuisines]
        }
        menu_item_list.append(menu_item_data)
    return jsonify({'menu_items': menu_item_list})


# Custom error handler for 404 Page Not Found
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    setup_database()
    app.run(host = '0.0.0.0', port = 5001,  debug=True)
