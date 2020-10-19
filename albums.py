import pickle
import requests
import os

def create_new_album(service, album_name):
    ''' Creates a new album of the given album name and returns the album ID '''
    request_body = {
        'album': {
            'title': album_name
        }
    }
    response = service.albums().create(body=request_body).execute()
    return response

def batch_create_images(service, album_path):
    ''' Takes the album path and uploads all images to Google's servers, then returns the response.
        The way the API works is that it first uploads the images to Google Photos, then you can
        use their IDs to add them to Google Photos albums
    '''

    # Stuff we need to make our post request
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
    token = pickle.load(open('token_photoslibrary_v1.pickle', 'rb'))
    headers = {
        'Authorization': 'Bearer ' + token.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw'
    }
    accepted_filetypes = ['BMP', 'GIF', 'HEIC', 'ICO', 'JPG', 'PNG', 'TIFF', 'WEBP', '3GP', '3G2', 'ASF', 'AVI', 'DIVX', 'M2T', 'M2TS', 'M4V', 'MKV', 'MMV', 'MOD', 'MOV', 'MP4', 'MPG', 'MTS', 'TOD', 'WMV']
    # Modifying the filetypes to be in the correct formula (because I'm lazy. Change them from the source if needed)
    accepted_filetypes = ['.' + filetype.lower() for filetype in accepted_filetypes]

    # Iterate over the images in the album and add them to the request body
    new_media_items = []
    for entry in os.scandir(album_path):
        # Evaluate if the file is one of the accepted filetypes
        proper_filetype = False
        for filetype in accepted_filetypes:
            proper_filetype = proper_filetype or entry.path.endswith(filetype)
        
        if (proper_filetype and entry.is_file()):
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

    request_body  = {
        'newMediaItems': new_media_items
    }

    response = service.mediaItems().batchCreate(body=request_body).execute()
    return response

def add_photos_to_album(service, album_path, album_id):
    ''' Adds all photos in the album path to the album of the given album ID.'''

    upload_url = f'https://photoslibrary.googleapis.com/v1/albums/{album_id}:batchAddMediaItems'
    token = pickle.load(open('token_photoslibrary_v1.pickle', 'rb'))
    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + token.token
    }
    upload_response = batch_create_images(service, album_path)
    new_media_item_results = upload_response['newMediaItemResults']
    media_item_ids = [new_media_item_result['mediaItem']['id'] for new_media_item_result in new_media_item_results]
    request_body = {
        'mediaItemIds': media_item_ids
    }
    response = requests.post(upload_url, data=request_body, headers=headers)
    return response


def check_album_exists(service, album_name):
    ''' Checks if an album of the given name already exists. If it does, return the album ID. Else return None. '''
    response_albums_list = service.albums().list().execute()
    albums_list = response_albums_list.get('albums')
    album_id_list = list(filter(lambda x: album_name in x['title'], albums_list))
    if len(album_id_list) == 0:
        return None

    return album_id_list[0]['id']