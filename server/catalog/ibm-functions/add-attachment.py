import cv2
import base64
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from cloudant.client import Cloudant
from cloudant.error import CloudantException

# def main():
#     client = Cloudant.iam(
#                 account_name="516178ef-46af-4c3f-b149-4740eaabf89e-bluemix",
#                 api_key="vzhNu-YSn2YZf4JQ0rXcqAbnE1iYIItmnfglmgYYvZCP",
#                 connect=True,
#             )
#     service = CloudantV1.new_instance(
#         account_name="516178ef-46af-4c3f-b149-4740eaabf89e-bluemix",
#         api_key="vzhNu-YSn2YZf4JQ0rXcqAbnE1iYIItmnfglmgYYvZCP",
#         connect=True,
#     )
#     my_database = client['maed-restaurants']
#     detailed_description = "Main image"
#     response = service.put_attachment(
#     db=my_database,
#     doc_id="6dfd73d203377a73f18d19f432b8bcc4",
#     attachment_name='barbecue-1239434_1920.jpg',
#     attachment=detailed_description,
#     content_type='image/jpeg'
#     ).get_result()

#     print(response)

# main()

def main(dict):
    client = Cloudant.iam(
        account_name="516178ef-46af-4c3f-b149-4740eaabf89e-bluemix",
        api_key="vzhNu-YSn2YZf4JQ0rXcqAbnE1iYIItmnfglmgYYvZCP",
        connect=True,
    )

    my_database = client['maed-restaurants']
    my_document = my_database[dict['document_id']]

    my_document.put_attachment(
        attachment=dict['img_name'],
        content_type='image/jpeg',
        data=dict['b64_string']
    )
    attachment = my_document.get_attachment(attachment=dict['img_name'])

    if attachment is not None:
        return {'status':'SUCCESS!!'}
    else:
        return {'status':'UPLOAD UNSUCCESSFUL'}

    # except CloudantException as ce:
    #     print("unable to connect")
    #     return {"error": ce}
    # except (requests.exceptions.RequestException, ConnectionResetError) as err:
    #     print("connection error")
    #     return {"error": err}

    # if my_document.exists():
    #     return {'status':'SUCCESS!!'}
main()

