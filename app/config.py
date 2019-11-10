hostname = {
    'PROD': 'host',
    'DEV': 'DESKTOP-6MT1J9I'
}

database_conn = {
    'PROD': {
        'user': 'jsnarvasa',
        'password': 'owX$y1%Jh5d1DW%vax',
        'host': 'localhost',
        'schema': 'CornAndCheese'
    },
    'DEV': {
        'user': 'root',
        'password': 'reZ9pTFAOyU8PVpQ@6UY4*k^jshcPojFHacV8x@aHKEORN@$G1',
        'host': 'localhost',
        'schema': 'CornAndCheese'
    }
}

mapbox = {
    'TOKEN': {
        'PROD': 'pk.eyJ1IjoianNuYXJ2YXNhIiwiYSI6ImNrMnNvZGF0cjBobnMzaHI2Y2JnNHowYzkifQ.sanfPV1Q18NtgNtnYAd9hg',
        'DEV': 'pk.eyJ1IjoianNuYXJ2YXNhIiwiYSI6ImNrMjdsYnFxZzBpb2YzY29qaTVjdXZ6OWkifQ.Tjk5Yjbs0sN4Sbe4tfCs6A'
    },
    'REVERSE_GEOCODING': 'https://api.mapbox.com/geocoding/v5/mapbox.places/'
}

photos = {
    'ALLOWED_EXTENSIONS' : {'jpg', 'jpeg'},
    'UPLOAD_DIRECTORY' : 'photos',
    'TEMP_FILENAME' : 'staging',
    'THUMBNAIL_PORTRAIT' : (400, 600),
    'THUMBNAIL_LANDSCAPE' : (600, 400),
    'THUMBNAIL_DIRECTORY' : 'thumbnail'
}