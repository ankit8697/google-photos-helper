import sys
from init_photo_service import connect_to_api
from albums import create_new_album, check_album_exists, recursively_add_photos_to_album

# setting ideas:
# recursively name (each new album is named after parent dir and then its own name)
# create albums for empty folders
# file name regex filter

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    if path is None:
        print("Please include a directory in the arguments")
        return
    default_album_name = sys.argv[2] if len(sys.argv) > 2 else None
    if default_album_name is None:
        # get the name of the dir at the path. i do the two splits here to make sure it works for / or \
        name_of_path_dir = path.split("/")[-1].split("\\")[-1].replace("/", "").replace("\\", "")
        default_album_name = name_of_path_dir

    service = connect_to_api()
    existing_album = check_album_exists(service, default_album_name)
    album = create_new_album(service, default_album_name) if existing_album is None else existing_album
    if album is None:
        print("Unable to create album ", default_album_name)
        return

    recursively_add_photos_to_album(service, path, album)

if __name__ == "__main__":
    main()