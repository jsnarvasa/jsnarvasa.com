import os
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
    FileName = db.Column('FileName', db.String(100), nullable=False, unique=True) # Hashed value of photo
    Caption = db.Column('Caption', db.String(5000))
    Upload_Date = db.Column('Upload_Date', db.Date, nullable=False) # Automatically added by the inserter
    Capture_Date = db.Column('Capture_Date', db.Date) # Date photo taken
    Place = db.Column('Place', db.String(150))
    City = db.Column('City', db.String(150))
    Region = db.Column('Region', db.String(6))
    Country = db.Column('Country', db.String(2))


    @classmethod
    def get_photo_list(cls, currentPage=1, perPage=9, start_date=None, end_date=None):
        # Output - Returns LIST of Photos objects
        currentPage = int(currentPage)
        if start_date is not None and end_date is not None:
            return cls.query.filter(Photos.Capture_Date.between(start_date, end_date)).order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items
        else:
            return cls.query.order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items

    @classmethod
    def search_photo_list(cls, searchQuery, currentPage=1, perPage=9, start_date=None, end_date=None):
        # Output - Returns multiple Photos objects, where geography matches the searchQuery
        currentPage = int(currentPage)
        if start_date is not None and end_date is not None:
            return cls.query.filter(Photos.Capture_Date.between(start_date, end_date), (Photos.Country.like('%' + searchQuery + '%')) | (Photos.City.like('%' + searchQuery + '%')) | (Photos.Place.like('%' + searchQuery + '%'))).order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items
        else:
            return cls.query.filter((Photos.Country.like('%' + searchQuery + '%')) | (Photos.City.like('%' + searchQuery + '%')) | (Photos.Place.like('%' + searchQuery + '%'))).order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items
    
    @classmethod
    def filter_photo_area(cls, searchQuery, currentPage=1, perPage=9, start_date=None, end_date=None):
        # Output - Returns multiple Photos objects, function is similar to search_photo_list, except focused on countries and regions only
        currentPage = int(currentPage)
        if start_date is not None and end_date is not None:
            return cls.query.filter(Photos.Capture_Date.between(start_date, end_date), (Photos.Country == searchQuery) | (Photos.Region == searchQuery)).order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items
        else:
            return cls.query.filter((Photos.Country == searchQuery) | (Photos.Region == searchQuery)).order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items

    @classmethod
    def search_photo_filename(cls, filename):
        # Output - Returns single Photos object, that matches filename
        return cls.query.filter_by(FileName=filename).first()

    @classmethod
    def get_time(cls, operation=None):
        if operation == 'min':
            min = db.session.query(db.func.min(Photos.Capture_Date)).first()
            return min[0]
        elif operation == 'max':
            max = db.session.query(db.func.max(Photos.Capture_Date)).first()
            return max[0]
        else:
            return None

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
        country, region = None, None
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

    @staticmethod
    def rotate_photo(img):
        try:
            for orientation in TAGS.keys():
                if TAGS[orientation]=='Orientation':
                    break

            exif=dict(img._getexif().items())

            if exif[orientation] == 3:
                img=img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img=img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img=img.rotate(90, expand=True)

            return img

        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            return img

    @classmethod
    def get_photo_dimensions(cls, photo):
        with Image.open(photo) as img:
            img = cls.rotate_photo(img)
            width, height = img.size
        return (width, height)

    @classmethod
    def generate_thumbnail(cls, photo, width, height):
        if width > height:
            size = config.photos['THUMBNAIL_LANDSCAPE']
        elif height > width:
            size = config.photos['THUMBNAIL_PORTRAIT']
        image = Image.open(photo)
        image = cls.rotate_photo(image)
        image.thumbnail(size, Image.ANTIALIAS)
        filename = os.path.basename(photo)
        thumbnail_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'photos', config.photos['THUMBNAIL_DIRECTORY'])
        image.save(os.path.join(thumbnail_dir, filename), 'JPEG')