import base64
# import cv2
import requests
from cloudant.client import Cloudant
import boto3
import random, string

# def base64_encode(img_dir):
#     img = cv2.imread(img_dir)
#     if img is None:
#         print("Could not read the image.")
#     jpg_img = cv2.imencode('.jpg', img)
#     b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
#     return b64_string

def retrieve_img(document_id, img_name):
    client = Cloudant.iam(
        account_name="516178ef-46af-4c3f-b149-4740eaabf89e-bluemix",
        api_key="vzhNu-YSn2YZf4JQ0rXcqAbnE1iYIItmnfglmgYYvZCP",
        connect=True,
    )
    my_database = client['maed-restaurants']
    my_document = my_database[document_id]
    img_data=my_document.get_attachment(attachment=img_name)

    image = base64.decodebytes(img_data)
    return image

def retrieve_all_documents():
    client = Cloudant.iam(
        account_name="516178ef-46af-4c3f-b149-4740eaabf89e-bluemix",
        api_key="vzhNu-YSn2YZf4JQ0rXcqAbnE1iYIItmnfglmgYYvZCP",
        connect=True,
    )
    my_database = client['maed-restaurants']
    my_documents = []
    for document in my_database:
        my_documents.append(document)
    return my_documents

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

def upload_image_s3(image, activity_name):
    client = boto3.client('s3',
        aws_access_key_id = '',
        aws_secret_access_key = '')

    randomstring = randomword(10)
    image_name = activity_name + '-' + randomstring + '.jpg'

    response = client.upload_fileobj(image, 'maed-d43-images', image_name)

    url = "https://maed-d43-images.s3.eu-central-1.amazonaws.com/" + image_name
    return url

def add_restaurant(restaurant):
    payload = {}
    payload['restaurant'] = {
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

def search(searchtxt):
    req_documents = []
    my_documents = retrieve_all_documents()
    keywords = searchtxt.split()
    for document in my_documents:
        for category in document['categories']:
            categories = ''
            categories = category + ' ' + categories
        for keyword in keywords:
            if keyword in document['name'].casefold() or keyword in categories.casefold() or keyword in document['details']['about'].casefold() or keyword in document['details']['features'].casefold():
                req_documents.append(document)
                break

    for req_document in req_documents:
        req_document['id'] = req_document.pop('_id')

    return req_documents

# req_documents = search('smoking')
# for test in req_documents:
#     print(test['name'])

def category_filter(selected_categories):
    req_documents = []
    documents = retrieve_all_documents()
    for document in documents:
        for category in selected_categories:
            if category in document['categories']:
                req_documents.append(document)
                break
    for document in req_documents:
        document['id'] = document.pop('_id')
    return req_documents
