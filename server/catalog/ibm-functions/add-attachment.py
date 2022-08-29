# import cv2
# import base64
# import sys
# from ibmcloudant.cloudant_v1 import CloudantV1
# from cloudant.client import Cloudant
# from cloudant.error import CloudantException

# def main(dict):
#     client = Cloudant.iam(
#         account_name="516178ef-46af-4c3f-b149-4740eaabf89e-bluemix",
#         api_key="vzhNu-YSn2YZf4JQ0rXcqAbnE1iYIItmnfglmgYYvZCP",
#         connect=True,
#     )

#     my_database = client['maed-restaurants']
#     my_document = my_database[dict['document_id']]

#     my_document.put_attachment(
#         attachment=dict['img_name'],
#         content_type='image/jpeg',
#         data=dict['b64_string']
#     )
#     attachment = my_document.get_attachment(attachment=dict['img_name'])

#     if attachment is not None:
#         return {'status':'SUCCESS!!'}
#     else:
#         return {'status':'UPLOAD UNSUCCESSFUL'}
# main()

