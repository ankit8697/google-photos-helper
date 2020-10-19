import sys
from init_photo_service import connect_to_api

def main():
    path = sys.argv[1]
    service = connect_to_api()
