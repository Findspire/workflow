# Create : POST
# /media/PARENT_MEDIA_UUID/
output : {
    'media_uuid'             : MEDIA_UUID,
    'parent_media_uuid'      : null | PARENT_MEDIA_UUID, # ex: Tracks in album
    'parent_profile_uuid'    : PARENT_PROFILE_UUID,
    'creation_date'          : TIMESTAMP, # Also used to sort results
    'type'                   : 'image | video | album | ...',
    'role'                   : 'image | profile_picture | ...', # Optional, used to create default boxes
    'status_code'       : 'HTTP_200_OK'
}

# Update media : PUT
# /media/MEDIA_UUID/
input : {
    'type' : 'image' # album article image track video
    'objects': {
        'background_image' : {
            '1x1' : {
                'x'      : 20,
                'y'      : 30,
                'height' : 542,
                'width'  : 645
            }
        }
    }
    'metadata'      : { # TODO
                        'title'         : 'Lys',
                        'description'   : 'A beautiful flower',
                      },
    'communities'   : ['image', 'video', ...]
    'tags'          : [''],
    'publication'   : null | {'publication_date' : TODO },
    'collection'    : '' | COLLECTION_UUID
}
output : {
    'status_code'   : 'HTTP_200_OK',
    'message'       : ''#'' FIXME : Gestion of language
}

# List media : GET
# /media/
input : # FIXME : May need filtering
output : {
    'MEDIA_UUID' : {
        'creation_date'     : TIMESTAMP, # Also used to sort results
        'parent_media'      : null | MEDIA_UUID, # ex: Tracks in album
        'parent_profile'    : PROFILE_UUID,
        'type'              : 'image | video | audio | article',
        'progress'          : 42,
        'status'            : 'pending | uploading | processing | complete',
        'publication'       : null | {'publication_date' : TODO},
        'collection'        : COLLECTION_UUID,
    },
    'status_code'       : 'HTTP_200_OK',
    'message'           : ''# FIXME : Gestion of language
}

# Read media : GET
# /media/MEDIA_UUID/
output : {
    'media_uuid'        : MEDIA_UUID,
    'parent_media'      : null | MEDIA_UUID, # ex: Tracks in album
    'parent_profile'    : PROFILE_UUID,
    'creation_date'     : TIMESTAMP, # Also used to sort results
    'type'              : 'image | video | audio | article',
    'metadata_form_url' : '/profile/PROFILE_UUID/MEDIA_TYPE/MEDIIA_UUID/metadata/', # all variables are known, is it realy useful ?
    'objects': {
        'background_image' : {
            'files' : {
                'source' : {
                    'url' : ['http://.*','http://.*'],
                },
                '1x1' : {
                    'url' : 'http://.*',
                    'metadata'  : {
                        'x'      : 20,
                        'y'      : 30,
                        'height' : 542,
                        'width'  : 645
                    },
                }
            }
        }
    }
    'metadata'      : { # TODO
                        'title'         : 'Lys',
                        'description'   : 'A beautiful flower',
                      },
    'inspirations_count': 0,
    'status'        : 'pending | uploading | processing | complete',
    'progress'      : 100,
    'tags'          : [''],
    'publication'   : null | { 'publication_date' : TODO },
    'collection'    : COLLECTION_UUID,
    'status_code'   : 'HTTP_200_OK'
    'message'       : ''# FIXME : Gestion of language
}

# Delete media : DELETE
# /media/MEDIA_UUID/
output :
    'status_code'   : 'HTTP_200_OK',
    'message'       : ''# FIXME : Gestion of language


# Initiate upload: POST
# /upload/MEDIA_UUID/object_type/
# Once the upload is complete, the file will be known as objects/files/<OBJECT_TYPE>/source.
input: {
    'size': 2097152,  # Size of the uploaded, file in bytes
}
output: {
    'media_uuid': MEDIA_UUID,
    'validity': 86400,     # Validity of the URLs, in seconds
    'part_size': 5000000,  # Size of a part, in bytes
    'urls': [
        'http://...',
        'http://...',
        'http://...'
    ],
    'parts': {
        '0': { 'status': 'waiting' },
        '1': { 'status': 'waiting' },
        '2': { 'status': 'waiting' }
    }
}

# Update an upload: PUT
# /upload/MEDIA_UUID/object_type/
input: {
    'parts': {
        '2': {
            'status': 'started | waiting | cancelled'  # If "cancelled", this will abort the whole upload.
        },
        '1': {
            'status': 'done',
            'size': 12345,
            'etag': 'abc123'   # Value of the "ETag" header in the response from the storage provider
        }
    }
}
output: {
    'status_code': 'HTTP_200_OK',
    'media_uuid': MEDIA_UUID,
    'parts': {
        '0': { 'status': 'waiting' },
        '1': {
            'status': 'done',
            'size': 12345,
            'etag': 'abc123'
         },
        '2': {
            'status': 'started | waiting | cancelled'
        }
    }
}

# Get new URLs: GET
# /upload/MEDIA_UUID/object_type/
input: first=2  # optional (defaults to 1); in query string
output: {
    'media_uuid': MEDIA_UUID,
    'parts': {
        '0': { 'status': 'waiting' },
        '1': { 'status': 'waiting' },
        '2': { 'status': 'waiting' }
    }
    'urls': {
        '2': 'http://...',
        '3': 'http://...'
    }
}

# Abort an upload: DELETE
# /upload/MEDIA_UUID/object_type/
# (same thing as setting any part to "cancelled")
output: {
    'status_code': 'HTTP_204_NO_CONTENT'
}


###################
### Collections ###
###################

# Create a new collection: PUT
# /collections/?profile_uuid=...
input: {
    'type': 'image|video|music',
    'name': '...',
    'description': '...'
}
output: {
    'collection_uuid': '...'
}

# Update a collection: POST
# /collections/COLLECTION_UUID
input: {
    'name': '...',
    'description': '...',
    'media_uuids': ['...', '...', ...]
}

# List all collections from a profile: GET
# /collections/?profile_uuid=...
output: {
    'collections': [
        {
            'collection_uuid': '...',
            'profile_uuid': '...',
            'name': '...',
            'description': '...',
            'type': '...',
            'creation_date': '...',
            'media_uuids': ['...', '...', ...]
        }, ...
    ]
}

# Get details about a single collection: GET
# /collections/COLLECTION_UUID/
output: {
    'collection_uuid': '...',
    'profile_uuid': '...',
    'name': '...',
    'description': '...',
    'type': '...',
    'creation_date': '...',
    'media_uuids': ['...', '...', ...]
}

# Delete a collection: DELETE
# /collections/COLLECTION_UUID/
