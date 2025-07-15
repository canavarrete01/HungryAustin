#!/usr/bin/env python3

# ---------------------------
# projects/IDB3/models.py
# 
# ---------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# initializing Flask app 
app = Flask(__name__) 

app.app_context().push()
USER ="postgres"
PASSWORD ="123"
PUBLIC_IP_ADDRESS ="localhost:5432"
DBNAME ="hungryaustindb"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_STRING', 'postgresql://postgres:123@localhost:5432/hungryaustindb')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/hungry_austin_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)


# Association table for the many-to-many relationship of cuisines and restaurants
restaurant_cuisine = db.Table('restaurant_cuisine',
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurants.id'), primary_key=True),
    db.Column('cuisine_id', db.Integer, db.ForeignKey('cuisines.id'), primary_key=True)
)

# Association table for the many-to-many relationship of menu_items and cuisines
menu_item_cuisine = db.Table('menu_item_cuisine',
    db.Column('menu_item_id', db.Integer, db.ForeignKey('menu_items.id'), primary_key=True),
    db.Column('cuisine_id', db.Integer, db.ForeignKey('cuisines.id'), primary_key=True)
)



class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.Text)
    location = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    tags = db.Column(db.Text)
    rating = db.Column(db.Float)

    # Relationship to cuisine (many-to-many)
    cuisines = db.relationship('Cuisine', secondary=restaurant_cuisine, back_populates="restaurants")


class Cuisine(db.Model):
    __tablename__ = 'cuisines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # JSON or string serialized fields for countries and flags
    countries = db.Column(db.Text)
    flags = db.Column(db.Text)

    # Relationship to Restaurant (many-to-many)
    restaurants = db.relationship('Restaurant', secondary=restaurant_cuisine, back_populates="cuisines")
    # Relationship to MenuItem (many-to-many)
    menu_items = db.relationship('MenuItem', secondary=menu_item_cuisine, back_populates='cuisines')


class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text)
    calories = db.Column(db.Integer)
    dietary = db.Column(db.Text) 
    # Relationship to Cuisine (many-to-many)
    cuisines = db.relationship('Cuisine', secondary=menu_item_cuisine, back_populates='menu_items')

    image = db.Column(db.Text) 


db.create_all()
