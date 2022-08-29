# from cloudant.client import Cloudant
# from cloudant.error import CloudantException
# import requests


# def main(dict):
#     try:
#         client = Cloudant.iam(
#             account_name="516178ef-46af-4c3f-b149-4740eaabf89e-bluemix",
#             api_key="vzhNu-YSn2YZf4JQ0rXcqAbnE1iYIItmnfglmgYYvZCP",
#             connect=True,
#         )
#         print("Databases: {0}".format(client.all_dbs()))
#         my_database = client['maed-restaurants']
#         my_document = my_database.create_document(dict["restaurant"])
#     except CloudantException as ce:
#         print("unable to connect")
#         return {"error": ce}
#     except (requests.exceptions.RequestException, ConnectionResetError) as err:
#         print("connection error")
#         return {"error": err}

#     if my_document.exists():
#         return {'status':'SUCCESS!!'}