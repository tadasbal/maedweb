from django.db import models

class Restaurant:

    def __init__(self, name, user, categories, reviews, contacts, details, menu_link, image_url):
        self.name = name
        self.user = user
        self.categories = categories
        self.reviews = reviews
        self.contacts = contacts
        self.details = details
        self.menu_link = menu_link
        self.image_url = image_url

    def __str__(self):
        return "Restaurant name: " + self.name


class Categories:
    
    restaurant_categories = ["Most Popular", "Fast Food", "Italian", "Grill", "Pasta", "Breakfast", "New", "Lithuanian", "Meat"]
    entertainment_categories = ["Most Popular", "New", "Swimming", "Bowling", "Outdoors", "Indoors", "Sports", "Active", "Cinema"]
    event_categories = ["Most Popular", "New", "Family", "Concert", "Outdoors", "Indoors", "Sports", "Active", "Other"]
