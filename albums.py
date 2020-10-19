def create_new_album(service, album_name):
    request_body = {
        'album': {
            'title': album_name
        }
    }
    response = service.albums().create(body=request_body).execute()
    return response

# def add_photo_to_album(service, photos):
#     pass