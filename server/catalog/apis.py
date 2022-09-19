import base64
# import cv2
import requests
from cloudant.client import Cloudant
import boto3
import random, string
# from dotenv import load_dotenv
import os

# def base64_encode(img_dir):
#     img = cv2.imread(img_dir)
#     if img is None:
#         print("Could not read the image.")
#     jpg_img = cv2.imencode('.jpg', img)
#     b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
#     return b64_string

def connect_cloudant():
    # load_dotenv()
    client = Cloudant.iam(
        account_name=os.environ.get("CLOUDANT_ACCOUNT_NAME"),
        api_key=os.environ.get("CLOUDANT_API_KEY"),
        connect=True,
    )
    return client

def connect_aws():
    # load_dotenv()
    client = boto3.client('s3',
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY"))

    return client

def retrieve_img(document_id, img_name):
    client = connect_cloudant()
    my_database = client['maed-restaurants']
    my_document = my_database[document_id]
    img_data=my_document.get_attachment(attachment=img_name)

    image = base64.decodebytes(img_data)
    return image

def retrieve_all_documents(db_name):
    client = connect_cloudant()
    my_database = client[db_name]
    my_documents = []
    for document in my_database:
        my_documents.append(document)
    client.disconnect()
    return my_documents

def retrieve_one_document(document_id, database):
    client = connect_cloudant()
    my_database = client[database]
    document = my_database[document_id]
    client.disconnect()
    return document

def create_document(url, payload):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, json=payload, headers=headers)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    return response

# '../static/catalog/Images/Restaurants/barbecue-1239434_1920.jpg'

def add_attachment(url, payload):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    try:
        # Call get method of requests library with URL and parameters
        response = requests.put(url, json=payload, headers=headers)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    return response

# def user_activities(user):
#     user_documents = []
#     my_documents = retrieve_all_documents('maed-restaurants')
#     for document in my_documents:
#         if document['user'] == user:
#             document['id'] = document.pop('_id')
#             user_documents.append(document)

#     return user_documents

def user_activities(user, database):
    user_documents = []
    client = connect_cloudant()
    my_database = client[database]
    selector = {'user': {'$eq': user}}
    documents = my_database.get_query_result(selector)
    for document in documents:
        document['id'] = document.pop('_id')
        document['database'] = database
        user_documents.append(document)
    client.disconnect()
    return user_documents

def upload_image_s3(image, activity_name):
    client = connect_aws()

    randomstring = randomword(10)
    image_name = activity_name + '-' + randomstring + '.jpg'

    response = client.upload_fileobj(image, 'maed-d43-images', image_name)

    url = "https://maed-d43-images.s3.eu-central-1.amazonaws.com/" + image_name
    return url

def delete_image_s3(image_url):
    client = connect_aws()

    image_name = image_url.split('/')[-1]

    response = client.delete_object(
        Bucket='maed-d43-images',
        Key=image_name,
    )
    return response

def add_restaurant(restaurant, activity_type):
    payload = {}
    payload[activity_type] = {
        "user":restaurant.user,
        "name":restaurant.name,
        "categories":restaurant.categories,
        "reviews":restaurant.reviews,
        "contacts":restaurant.contacts,
        "details":restaurant.details,
        "menu_link":restaurant.menu_link,
        "image_url":restaurant.image_url
    }

    response = create_document("https://f116ae20.eu-de.apigw.appdomain.cloud/restaurants/create-document", payload)
    print(response.text)
    return response

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def search(searchtxt, activities):
    req_documents = []
    database = 'maed-' + activities
    my_documents = retrieve_all_documents(database)
    keywords = searchtxt.split()
    for document in my_documents:
        for category in document['categories']:
            categories = ''
            categories = category + ' ' + categories
        for keyword in keywords:
            if keyword.casefold() in document['name'].casefold() or keyword.casefold() in categories.casefold() or keyword.casefold() in document['details']['about'].casefold() or keyword.casefold() in document['details']['features'].casefold():
                req_documents.append(document)
                break

    for req_document in req_documents:
        req_document['id'] = req_document.pop('_id')

    return req_documents

# req_documents = search('smoking')
# for test in req_documents:
#     print(test['name'])

def category_filter(selected_categories, activities):
    req_documents = []
    database = 'maed-' + activities
    documents = retrieve_all_documents(database)
    for document in documents:
        for category in selected_categories:
            if category in document['categories']:
                req_documents.append(document)
                break
    for document in req_documents:
        document['id'] = document.pop('_id')
    return req_documents

def update_document(restaurant, document_edit, database):
    client = connect_cloudant()
    my_database = client[database]
    document = my_database[document_edit['_id']]
    document['name'] = restaurant.name
    document['categories'] = restaurant.categories
    document['contacts'] = restaurant.contacts
    document['details'] = restaurant.details
    document['menu_link'] = restaurant.menu_link

    if restaurant.image_url != '':
        document['image_url'] = restaurant.image_url

    document.save()
    client.disconnect()
    return document

def delete_document(document_id, database):
    client = connect_cloudant()
    my_database = client[database]
    document = my_database[document_id]
    document.delete()
    client.disconnect()
    return 'DOCUMENT SUCCESFULLY DELETED'




