import socket
import requests
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from app import db
import config

if socket.gethostname() == config.hostname['PROD']:
    host = 'PROD'
else:
    host = 'DEV'

class Photos(db.Model):
    __tablename__ = 'Photos'

    PhotoID = db.Column('PhotoID', db.Integer, primary_key=True, autoincrement=True)
    FileName = db.Column('FileName', db.String(100), nullable=False, unique=True)
    Caption = db.Column('Caption', db.String(5000))
    Upload_Date = db.Column('Upload_Date', db.Date, nullable=False)
    Capture_Date = db.Column('Capture_Date', db.Date)
    Place = db.Column('Place', db.String(150))
    City = db.Column('City', db.String(150))
    Region = db.Column('Region', db.String(6))
    Country = db.Column('Country', db.String(2))


    @classmethod
    def get_photo_list(cls, currentPage=1, perPage=9):
        currentPage = int(currentPage)
        return cls.query.order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items

    @classmethod
    def search_photo_list(cls, searchQuery, currentPage=1, perPage=9):
        currentPage = int(currentPage)
        return cls.query.filter((Photos.Country.like('%' + searchQuery + '%')) | (Photos.City.like('%' + searchQuery + '%')) | (Photos.Place.like('%' + searchQuery + '%'))).order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items
        
    @classmethod
    def search_photo_filename(cls, filename):
        return cls.query.filter_by(FileName=filename).first()

    @staticmethod
    def check_allowed_filetype(filename):
    # Output - Returns boolean based on whether file's filetype is allowed
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.photos['ALLOWED_EXTENSIONS']
    
    @staticmethod
    def photo_hash(filename):
        photo = open(filename, 'rb').read()
        return hashlib.md5(photo).hexdigest()

    @staticmethod
    def get_exif(filename):
    # Input - Filename of image (incl. absolute path)
    # Output - Image EXIF data
        image = Image.open(filename)
        image.verify()
        return image._getexif()

    @staticmethod
    def get_geotagging(exif):
        geotagging = {}
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx not in exif:
                    raise ValueError("No EXIF geotagging found")

                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]
        
        return geotagging

    @staticmethod
    def get_decimal_from_dms(dms, ref):
    # Input - GPS coordinate in Degrees, Minutes, Seconds notation
    # Output - GPS coordinate in decimal notation

        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0

        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds

        return round(degrees + minutes + seconds, 5)

    @classmethod
    def get_coordinates(cls, geotags):
    # Output - Returns GPS coordinates in (latitude, longitude) decimal notation TUPLE format
        lat = cls.get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
        lon = cls.get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
        return (lat,lon)

    @staticmethod
    def reverse_geocode(coordinates):
        url = config.mapbox['REVERSE_GEOCODING'] + str(coordinates[1]) + ',' + str(coordinates[0]) + '.json'
        if host == 'PROD':
            parameters = {'access_token' : config.mapbox['TOKEN']['PROD']}
        else:
            parameters = {'access_token' : config.mapbox['TOKEN']['DEV']}
        response = requests.get(url, params=parameters)
        if response.status_code == 200:
            response = response.json()
            for feature in response['features']:
                feature_type = feature['id'].split('.')
                if feature_type[0] == 'country':
                    country = feature['properties']['short_code'].upper()
                elif feature_type[0] == 'region':
                    region = feature['properties']['short_code'].upper()
        else:
            raise Exception
        return (region, country)
