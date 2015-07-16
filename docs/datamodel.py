

PUBLICATION = {
    'publication_status': 'published',
    'publication_date'  : '2012-11-24T23:27:01.123456'
}

COMMENTS = {
      'uuid' : uuid5_b64,
      'comments' : [ {
            'publication'   : PUBLICATION,
            'text'          : "This is the best Camera I've used so far",
      }, {
            'publication'   : PUBLICATION,
            'text'          : "Did you try the new RED ??"
      }]
}

GEOLOCATION = {
        'continent' : 'europe',
        'country'   : 'france',
        'region'    : 'lorraine',
        'city'      : 'Nancy',
        'gps'       : """48"41'34.695N6"10'53.023E""",
}

CONTRIBUTION = {
      'light'  : {
          'user_fullname' : "Florent Defayte",
          'user_uuid'     : "florent.defayte"
      },
      'set'     : [ {
          'user_fullname' : "Sacha Tremoureux",
          'user_uuid'     : "sacha.tremoureux",
          'role'          : "Indoor'",
      }, {
          'user_fullname' : "Sebvastien Duboc",
          'user_id'       : "sebastien.duboc",
          'role'          : "Outdoor"
      } ]
  }



COMMENTS_INFO = { 
    'comments_count'     : 1235,
    'comments_uuid'      : COMMENTS_uuid5_b64,
}

FILES = {
    's3'        :  [{
        'zone'    : 'europe',
        'bucket'  : 'findspire_S3UUIDlowercase',
        'objects' : {
            'preview_1x1' : {
                'name' : '1x1_image.jpg',
                'type' : 'jpg'
            }
            'original' : {
                'name' : 'original.png',
                'type' : 'png'
            }
        }]
    },
    'findspire'        :  [{
        'zone'    : 'europe',
        'bucket'  : 'findspire_UUID64',
        'objects' : {
            'preview_1x1' : {
                'name' : '1x1_image.jpg',
                'type' : 'jpg'
            }
            'original' : {
                'name' : 'original.png',
                'type' : 'png'
            }
        }
    }]
}

GEOMETRY = {
        'width'  : 34124,
        'height' : 3123,
        'ratio'  : '16/9'
}

METADATA = {
        'title'         : 'Title',
        'description'   : 'A beautiful flower',
        'duration'      : '102',
        'geometry'      : GEOMETRY,
        'contributions' : CONTRIBUTIONS,
        'language'      : 'fr'
}

CATEGORIES = {
    'primary' : 'B&W',
    'others'  : ['cats', 'paris']
}



Medias = {
      'media_uuid'        : media_uuid,
      'type'              : 'image|video|album|track|article',
      'parent_profile'    : profile_uuid,
      'tracks'            : { 1 : media_uuid, ...},
      'inspirations_count': 1243,
      'comments_info'     : COMMENTS_INFO,
      'geolocation'       : GEOLOCATION,
      'files'             : FILES,
      'metadata'          : METADATA,
      'communities'       : ['video', 'music'],
      'categories'        : CATEGORIES
      'tags'              : ['picture', 'french', 'sextape']
  }

ACLS = {
    'user_uuid'       : {
         'edit'    : true,
         'delete'  : false,
         'publish' : false
    }
}

Profiles = {
    'profile_uuid'      : uuid5_b64,
    'owner_uuid'        : uuid5_b64,
    'parent_profile'    : uuid5_b64, # Used for localized profiles
    'child_profiles'    : { child_profile_uuid : {
                              'geolocation'     : GEOLOCATION
                              'acls'            : ACLS,
                            }
                          }
    'inspirations_count': 1243,
    'type'              : 'movie|event|artist|professional|product',
    'picture'           : media_uuid,
    'comments_info'     : COMMENTS_INFO,
    'publication'       : PUBLICATION,
    'geolocation'       : GEOLOCATION,
    'metadata'          : METADATA,
    'communities'       : ['video', 'music'],
    'categories'        : CATEGORIES
    'tags'              : ['video', 'french', 'sextape']
    'releases'          : [ {
        'media_uuid'        : media_uuid,
        'publication'       : PUBLICATION,
    } ]
}

User = {
  'user_uuid'     : uuid5_b64,
  'type'          : 'artist|professionnal|passionate',
  'first_name'    : '',
  'last_name'     : '',
  'address'       : '',
  'zip_code'      : '',
  'city'          : '',
  'country'       : '',
  'email_address' : '',
  'birth_date'    : '',
  'pseudonym'     : '',
  'state'         : '',
  'sex'           : '',
  'situation'     : '',
  'phone'         : '',
}


##################################

