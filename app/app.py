from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime
import socket
import config


# Determining environment
hostname = socket.gethostname()

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
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
db = SQLAlchemy(app)

from models.Photos import Photos
from models.Countries import Countries


######################################################
# Routes
######################################################
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/photoblog")
def photoblog():
    image_names = Photos.get_photo_list()
    return render_template("gallery.html", image_names=image_names)


@app.route("/photoblog/<pageNum>")
def photoblog_pageNum(pageNum):
    image_names = Photos.get_photo_list(pageNum)
    image_list = []
    for image in image_names:
        image_list.append(image.FileName)
    return jsonify(image_names=image_list)


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
    return render_template('gallery.html', image_names=image_names, searchQuery=searchQuery)


@app.route("/search/<pageNum>", methods=["GET"])
def search_pageNum(pageNum):
    searchQuery = request.args.get('q','')
    image_names = Photos.search_photo_list(searchQuery, pageNum, 9)
    image_list = []
    for image in image_names:
        image_list.append(image.FileName)
    return jsonify(image_names=image_list)


@app.route("/maps")
def maps():
    geojson = Countries.get_country(['US', 'AU', 'US'])
    geojson = Countries.geojson_constructor(geojson)
    return render_template('maps.html', country_geojson=geojson)


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
