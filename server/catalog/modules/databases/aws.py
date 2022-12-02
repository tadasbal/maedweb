"""Functions for handling images in AWS S3"""

import boto3
import random, string
import os

def connect_aws():
    """Connect to aws client"""

    client = boto3.client('s3',
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY"))

    return client

# Maybe i can put this function elsewhere?
def randomword(length):
    """Create random string for image naming"""

    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def upload_image_s3(image, activity_name):
    """Upload image to AWS S3"""

    client = connect_aws()

    randomstring = randomword(10)
    image_name = activity_name + '-' + randomstring + '.jpg'

    response = client.upload_fileobj(image, 'maed-d43-images', image_name)

    url = "https://maed-d43-images.s3.eu-central-1.amazonaws.com/" + image_name
    return url

def delete_image_s3(image_url):
    """Delete image from AWS S3"""

    client = connect_aws()

    image_name = image_url.split('/')[-1]

    response = client.delete_object(
        Bucket='maed-d43-images',
        Key=image_name,
    )
    return response
    