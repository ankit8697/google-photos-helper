import pickle
import requests
import os

from googleapiclient.errors import HttpError
from init_photo_service import connect_to_api


def create_new_album(service, album_name):
    """ Creates a new album of the given album name and returns the album ID """
    request_body = {
        'album': {
            'title': album_name
        }
    }
    response = service.albums().create(body=request_body).execute()
    return response['id']


def upload_batch_of_images(service, album_id, new_media_items):
    n = 50
    batched_media_items = [new_media_items[i:i + n] for i in range(0, len(new_media_items), n)]
    for batch in batched_media_items:
        request_body = {
            'albumId': f"{album_id}",
            'newMediaItems': batch
        }
        service.mediaItems().batchCreate(body=request_body).execute()


def batch_create_images(service, album_path, album_id):
    """ Takes the album path and uploads all images to Google's servers, adds them to the album_id, then returns the
        response, or None if there
        were no images.
    """

    # Stuff we need to make our post request
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
    token = pickle.load(open('token_photoslibrary_v1.pickle', 'rb'))
    headers = {
        'Authorization': 'Bearer ' + token.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw'
    }
    accepted_filetypes = ['BMP', 'GIF', 'HEIC', 'ICO', 'JPG', 'PNG', 'TIFF', 'WEBP', '3GP', '3G2', 'ASF', 'AVI', 'DIVX',
                          'M2T', 'M2TS', 'M4V', 'MKV', 'MMV', 'MOD', 'MOV', 'MP4', 'MPG', 'MTS', 'TOD', 'WMV']
    # Modifying the filetypes to be in the correct formula (because I'm lazy. Change them from the source if needed)
    accepted_filetypes = ['.' + filetype.lower() for filetype in accepted_filetypes]

    # Iterate over the images in the album and add them to the request body
    new_media_items = []
    for entry in os.scandir(album_path):
        # Evaluate if the file is one of the accepted filetypes
        proper_filetype = False
        for filetype in accepted_filetypes:
            proper_filetype = proper_filetype or entry.path.endswith(filetype)

        if proper_filetype and entry.is_file():
            print("Found media", entry.path)
            image_path = entry.path
            headers['X-Goog-Upload-File-Name'] = entry.name
            img = open(image_path, 'rb').read()
            # Upload image to Google's servers
            response = requests.post(upload_url, data=img, headers=headers)
            token = response.content.decode('utf-8')
            new_media_item = {
                'simpleMediaItem': {
                    'uploadToken': token
                }
            }
            new_media_items.append(new_media_item)

    if len(new_media_items) == 0:
        # don't do anything if there were no images
        return None

    try:
        upload_batch_of_images(service, album_id, new_media_items)
    except HttpError as err:
        print("Unable to upload items to album", album_path, ":", err)
        if "permission to add media items" in str(err.content):
            print("It looks like Photos Helper wasn't able to upload to this album. Tools like this are only able to "
                  "modify albums that were created automatically. If you already have an album with the same name as a "
                  "directory, that is probably the cause.")
    
    except BrokenPipeError as err:
        service = connect_to_api()
        upload_batch_of_images(service, album_id, new_media_items)
    return None


def recursively_add_photos_to_album(service, album_path, album_id):
    ''' Adds all photos in the album path to the album of the given album ID.'''
    print("New album:", album_path)
    batch_create_images(service, album_path, album_id)

    for entry in os.scandir(album_path):
        if entry.is_dir():
            existing_album = check_album_exists(service, entry.name)
            actual_album = create_new_album(service, entry.name) if existing_album is None else existing_album
            if actual_album is None:
                print("Unable to create album: ", entry.name)
                return
            recursively_add_photos_to_album(service, entry.path, actual_album)


def check_album_exists(service, album_name):
    ''' Checks if an album of the given name already exists. If it does, return the album ID. Else return None. '''
    response_albums_list = service.albums().list().execute()
    albums_list = response_albums_list.get('albums')
    album_id_list = list(filter(lambda x: album_name in x['title'], albums_list))
    if len(album_id_list) == 0:
        return None

    return album_id_list[0]['id']
