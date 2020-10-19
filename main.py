import sys
from init_photo_service import connect_to_api
from albums import create_new_album

def main():
    path = sys.argv[1]
    service = connect_to_api()
    create_new_album(service, "My New Album")
    
if __name__ == "__main__":
    main()