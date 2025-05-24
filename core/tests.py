from django.test import TestCase

# Create your tests here.
import requests

api_url = 'http://localhost:8000/rag/image/'
image_path = 'data/test.jpg'

with open(image_path, 'rb') as image_file:
    response = requests.post(api_url, files={'image': image_file})
    print(response)