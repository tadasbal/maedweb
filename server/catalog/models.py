from django.db import models

class Restaurant:

    def __init__(self, name, categories, reviews, contacts, details, menu_link):
        self.name = name
        self.categories = categories
        self.reviews = reviews
        self.contacts = contacts
        self.details = details
        self.menu_link = menu_link

    def __str__(self):
        return "Restaurant name: " + self.name

