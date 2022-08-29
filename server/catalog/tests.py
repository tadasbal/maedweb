from django.test import TestCase
# from django.http import FileResponse
# from .apis import add_attachment, base64_encode, create_document, retrieve_img
# from models import Restaurant

# def add_image(img_path, doc_id, img_name):
#     payload = {}
#     b64_string = base64_encode(img_path)
#     payload['document_id'] = doc_id
#     payload['img_name'] = img_name
#     payload['b64_string'] = b64_string
#     response = add_attachment("https://f116ae20.eu-de.apigw.appdomain.cloud/restaurants/add-attachment", payload)
#     return response

# def add_restaurant(rest_name, rest_categories):
#     restaurant = Restaurant
#     restaurant.name = rest_name
#     restaurant.categories = rest_categories
#     restaurant.reviews = {"Overall":4, "Food":4, "Price":5, "Service":3, "Place":4}
#     restaurant.contacts = {"address":"Pašilaičių g. 7, Vilnius", "phone":"+37068250572", "email":"something@gmail.com", "website":"www.something.com"}
#     restaurant.details = {"about":"In the a historic church build in 1768 in the heart of Vilnius is our restaurant ''Pirmas blynas'', literally translated to 'The first pancake'. We are a Pancake-house with a culinary and social mission. In our social restaurant your delicious pancakes are prepared and served by people with a disability. We are offering a variety of freshly made sweet and savoury pancakes, salads, a soup of the day and we serve coffee roasted by our own employees.",
#         "features":"Wifi, Cool Staff, Beautiful Interior, Takeout, Reservations, Outdoor Seating, Seating, Highchairs Available, Wheelchair Accessible, Free Wifi, Table Service, Street Parking, Free off-street parking, Playgrounds, Family style, Non-smoking restaurants, Gift Cards Available"}
#     restaurant.menu_link = "www.something.com"
#     payload = {}
#     payload['restaurant'] = {
#         "name":restaurant.name,
#         "categories":restaurant.categories,
#         "reviews":restaurant.reviews,
#         "contacts":restaurant.contacts,
#         "details":restaurant.details,
#         "menu-link":restaurant.menu_link
#     }

#     response = create_document("https://f116ae20.eu-de.apigw.appdomain.cloud/restaurants/create-document", payload)
#     print(response.text)
#     return response


# Create your tests here.
