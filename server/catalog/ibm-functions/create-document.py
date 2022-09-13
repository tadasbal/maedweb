# from cloudant.client import Cloudant
# from cloudant.error import CloudantException
# import requests


# def main(dict):
#     try:
#         client = Cloudant.iam(
#             account_name="",
#             api_key="",
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