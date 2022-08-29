import base64
# import cv2
import requests
from cloudant.client import Cloudant

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

    # with open("imageToSave.png", "wb") as fh:
    #     fh.write(base64.decodebytes(img_data))

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