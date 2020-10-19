import os
from google import create_service
 
API_NAME = 'photoslibrary'
API_VERSION = 'v1'
CLIENT_SECRET_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']

def connect_to_api():
    service = create_service(CLIENT_SECRET_FILE,API_NAME, API_VERSION, SCOPES)   
    return service       
