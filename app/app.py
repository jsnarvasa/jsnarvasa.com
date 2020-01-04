from flask import Flask, render_template, redirect, url_for, jsonify, request, flash, session
from werkzeug.utils import secure_filename
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime
from sqlalchemy import exc
from PIL import Image
import os
import socket
import config


# Environment
hostname = socket.gethostname()
dir_path = os.path.dirname(os.path.realpath(__file__))


######################################################
# Logging
######################################################
import logging

logs_dir_path = os.path.join(dir_path, 'logs')
log_file_path = os.path.join(logs_dir_path, 'web.log')
if not os.path.exists(logs_dir_path):
    os.makedirs(logs_dir_path)

logging.basicConfig(filename=log_file_path, level=logging.INFO)


######################################################
# Initialise Flask and SQLAlchemy classes
######################################################
app = Flask(__name__)
if hostname == config.hostname['PROD']:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + config.database_conn['PROD']['user'] + ':' + config.database_conn['PROD']['password'] + '@' + config.database_conn['PROD']['host'] + '/' + config.database_conn['PROD']['schema'] + '?charset=utf8mb4'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + config.database_conn['DEV']['user'] + ':' + config.database_conn['DEV']['password'] + '@' + config.database_conn['DEV']['host'] + '/' + config.database_conn['DEV']['schema'] + '?charset=utf8mb4'
    app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800

# Create photos upload directory
app.config['UPLOAD_FOLDER'] = config.photos['UPLOAD_DIRECTORY']
photo_upload_dir_path = os.path.join(dir_path, 'static', app.config['UPLOAD_FOLDER'])
if not os.path.exists(photo_upload_dir_path):
    os.makedirs(photo_upload_dir_path)
if not os.path.exists(os.path.join(photo_upload_dir_path, config.photos['THUMBNAIL_DIRECTORY'])):
    os.makedirs(os.path.join(photo_upload_dir_path, config.photos['THUMBNAIL_DIRECTORY']))

app.secret_key = os.urandom(128)
db = SQLAlchemy(app)

# Models
from models.Photos import Photos
from models.Area import Area
from models.Utilities import Utils


######################################################
# View Decorators
######################################################
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

######################################################
# Routes
######################################################
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/photoblog")
def photoblog():
    date_range = {}
    date_range['min'] = Photos.get_time('min')
    date_range['max'] = Photos.get_time('max')

    # To accommodate for timeline start and end date request
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    if start_date is not None and end_date is not None:
        image_names = Photos.get_photo_list(start_date=start_date, end_date=end_date)
    else:
        image_names = Photos.get_photo_list()
    
    geojson = Utils.get_geojson(image_names)
    token = Utils.get_mapbox_token(hostname)

    return render_template("gallery.html", image_names=image_names, geojson=geojson, token=token, date_range=date_range, start_date=start_date, end_date=end_date)


@app.route("/photoblog/<pageNum>")
def photoblog_pageNum(pageNum):
    
    # To accommodate for timeline start and end date request
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    if start_date is not None and end_date is not None:
        image_names = Photos.get_photo_list(pageNum, start_date=start_date, end_date=end_date)
    else:
        image_names = Photos.get_photo_list(pageNum)

    image_list = [image.FileName for image in image_names]
    geojson = Utils.get_geojson(image_names)

    return jsonify(image_names=image_list, geojson=geojson)


@app.route('/photoblog/area/<AreaCode>')
def area(AreaCode):
    image_names = Photos.search_photo_list(AreaCode)
    geojson = Utils.get_geojson(image_names)
    token = Utils.get_mapbox_token(hostname)

    return render_template('gallery.html', image_names=image_names, searchQuery=AreaCode, geojson=geojson, token=token)

@app.route("/getphotodetails")
def getphotodetails():
    filename = request.args.get('img', 'Error', type=str)
    image = Photos.search_photo_filename(filename)
    Caption = image.Caption
    Place = image.Place
    City = image.City
    Country = image.Country
    Upload_Date = image.Upload_Date.strftime("%A, %d %B %Y")
    Capture_Date = image.Capture_Date.strftime("%A, %d %B %Y")
    return jsonify(Caption=Caption, Place=Place, City=City, Country=Country,Upload_Date=str(Upload_Date), Capture_Date=str(Capture_Date))


@app.route("/search", methods=["GET"])
def search():
    searchQuery = request.args.get('q', '')
    image_names = Photos.search_photo_list(searchQuery)

    geojson = Utils.get_geojson(image_names)
    token = Utils.get_mapbox_token(hostname)

    return render_template('gallery.html', image_names=image_names, searchQuery=searchQuery, geojson=geojson, token=token)


@app.route("/search/<pageNum>", methods=["GET"])
def search_pageNum(pageNum):
    searchQuery = request.args.get('q','')
    image_names = Photos.search_photo_list(searchQuery, pageNum, 9)
    image_list = []
    for image in image_names:
        image_list.append(image.FileName)

    geojson = Utils.get_geojson(image_names)

    return jsonify(image_names=image_list, geojson=geojson)


@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        try:
            file = request.files['file']
        except Exception:
            flash("No image file was selected", "error")
            return redirect(request.url)
        
        if file and Photos.check_allowed_filetype(file.filename):
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1]
            
            # Save image file with staging filename
            staging_filename = config.photos['TEMP_FILENAME'] + '.' + file_extension
            file.save(os.path.join(photo_upload_dir_path, staging_filename))

            # Generate hashed filename for uploaded image, and rename from staging to hashed filename
            hashed_filename = Photos.photo_hash(os.path.join(photo_upload_dir_path, staging_filename)) + '.' + file_extension
            try:
                os.rename(os.path.join(photo_upload_dir_path, staging_filename), os.path.join(photo_upload_dir_path, hashed_filename))
            except FileExistsError:
                flash("File already exists", 'error')
                os.remove(os.path.join(photo_upload_dir_path, staging_filename))
                return redirect(request.url)
            
            # Obtain geolocation of uploaded image
            try:
                exif = Photos.get_exif(os.path.join(photo_upload_dir_path, hashed_filename))
                geotag = Photos.get_geotagging(exif)
                coordinates = Photos.get_coordinates(geotag)
                area = Photos.reverse_geocode(coordinates)
            except Exception:
                flash("Uploaded photo has invalid or no geolocation data")
                os.remove(os.path.join(photo_upload_dir_path, hashed_filename))
                return redirect(request.url)

            # Rotates the photo to the correct orientation.  Pillow also inadvertently strips all EXIF data
            image_file = Image.open(os.path.join(photo_upload_dir_path, hashed_filename))
            image_file = Photos.rotate_photo(image_file)
            image_file.save(os.path.join(photo_upload_dir_path, hashed_filename))

            photo = Photos(FileName=hashed_filename,
                Caption=request.form['caption'],
                Upload_Date=datetime.today().strftime('%Y-%m-%d'),
                Capture_Date=request.form['capture_date'],
                Place=request.form['place'],
                City=request.form['city'],
                Region=area[0],
                Country=area[1])
            try:
                db.session.add(photo)
            except exc.IntegrityError:
                flash("Photo already exists in the database")
                db.session.rollback()
                os.remove(os.path.join(photo_upload_dir_path, hashed_filename))
                return redirect(request.url)
            else:
                width, height = Photos.get_photo_dimensions(os.path.join(photo_upload_dir_path, hashed_filename))
                Photos.generate_thumbnail(os.path.join(photo_upload_dir_path, hashed_filename), width, height)
                db.session.commit()
                flash("Photo upload successful")
                return redirect(url_for('upload'))

        else:
            flash('Invalid file')
            return redirect(request.url)
            
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if request.form['username'] == 'jsnarvasa' and request.form['password'] == 'test':
            session['username'] = request.form['username']
            return redirect(url_for('upload'))
        else:
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # remove username from the session
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/sitemap')
def sitemap():
    return redirect(url_for('static',filename='sitemap.xml'))


@app.errorhandler(403)
def forbidden(e):
    return render_template('error/403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


# Setting variables to be called in the base template
# Ideal color #1894EB; color generated to be used by navbar
@app.context_processor
def generate_random_color():
    r = lambda: randint(0,50)
    g = lambda: randint(100,180)
    b = lambda: randint(180,220)
    color = '#%02X%02X%02X' % (r(),g(),b()) #string formatting used where 02 represents 2 values and padded by 0, X to return hex
    return dict(generated_color=color)
