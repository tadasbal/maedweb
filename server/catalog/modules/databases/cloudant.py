"""Functions for handling documents in Cloudant database"""

from cloudant.client import Cloudant
from cloudant.error import CloudantException
import os
import requests

def connect_cloudant():
    """Connect to cloudant client"""

    client = Cloudant.iam(
        account_name=os.environ.get("CLOUDANT_ACCOUNT_NAME"),
        api_key=os.environ.get("CLOUDANT_API_KEY"),
        connect=True,
    )
    return client

def retrieve_all_documents(db_name):
    """Retrieve all documents from cloudant"""

    client = connect_cloudant()
    my_database = client[db_name]
    my_documents = []
    for document in my_database:
        my_documents.append(document)
    client.disconnect()
    return my_documents

def retrieve_one_document(document_id, database):
    """Retrieve one document from cloudant"""

    client = connect_cloudant()
    my_database = client[database]
    document = my_database[document_id]
    client.disconnect()
    return document

def add_activity(activity):
    """Add document (activity) to cloudant"""

    try:
        client = connect_cloudant()
        my_database = client[f'maed-{activity.type}']
        my_database.create_document(activity.__dict__)
        client.disconnect()
        return {'status':'SUCCESS!!'}
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

def user_activities(user, database):
    """Filter and retrieve all user documents"""

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

def update_document(activity, document_edit, database):
    """Update document (activity) in cloudant"""

    client = connect_cloudant()
    my_database = client[database]
    document = my_database[document_edit['_id']]
    document['name'] = activity.name
    document['categories'] = activity.categories
    document['contacts'] = activity.contacts
    document['details'] = activity.details
    document['menu_link'] = activity.menu_link

    if activity.image_url != '':
        document['image_url'] = activity.image_url

    document.save()
    client.disconnect()
    return document

def delete_document(document_id, database):
    """Delete document (activity) from cloudant"""

    client = connect_cloudant()
    my_database = client[database]
    document = my_database[document_id]
    document.delete()
    client.disconnect()
    return 'DOCUMENT SUCCESFULLY DELETED'

def search(searchtxt, activities):
    """Search for documents according to client inputted text from cloudant"""
    
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

def category_filter(selected_categories, activities):
    """Filter documents from cloudant according to client's selected categories"""

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
