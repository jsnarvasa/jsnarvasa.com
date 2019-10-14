from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime
from config import database_conn


######################################################
# Initialise Flask and SQLAlchemy classes
######################################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + database_conn['user'] + ':' + database_conn['password'] + '@' + database_conn['host'] + '/' + database_conn['schema'] + '?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
db = SQLAlchemy(app)
from models.Photos import Photos


######################################################
# Routes
######################################################
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/photoblog")
def photoblog():
    image_names = Photos.query.order_by(Photos.Capture_Date.desc()).paginate(page=1, per_page=9, error_out=False)
    image_names = image_names.items
    return render_template("gallery.html", image_names=image_names)


@app.route("/photoblog/<pageNum>")
def photoblog_pageNum(pageNum):
    pageNum = int(pageNum)
    image_names = Photos.query.order_by(Photos.Capture_Date.desc()).paginate(page=pageNum, per_page=9, error_out=False)
    image_names = image_names.items
    image_list = []
    for image in image_names:
        image_list.append(image.FileName)
    return jsonify(image_names=image_list)


@app.route("/getphotodetails")
def getphotodetails():
    filename = request.args.get('img', 'Error', type=str)
    image = Photos.query.filter_by(FileName=filename).first()
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
    image_names = Photos.query.filter((Photos.Country.like('%' + searchQuery + '%')) | (Photos.City.like('%' + searchQuery + '%')) | (Photos.Place.like('%' + searchQuery + '%'))).order_by(Photos.Capture_Date.desc()).paginate(page=1, per_page=9, error_out=False)
    image_names = image_names.items
    return render_template('gallery.html', image_names=image_names, searchQuery=searchQuery)


@app.route("/search/<pageNum>", methods=["GET"])
def search_pageNum(pageNum):
    pageNum = int(pageNum)
    searchQuery = request.args.get('q','')
    image_names = Photos.query.filter((Photos.Country.like('%' + searchQuery + '%')) | (Photos.City.like('%' + searchQuery + '%')) | (Photos.Place.like('%' + searchQuery + '%'))).order_by(Photos.Capture_Date.desc()).paginate(page=pageNum, per_page=9, error_out=False)
    image_names = image_names.items
    image_list = []
    for image in image_names:
        image_list.append(image.FileName)
    return jsonify(image_names=image_list)


@app.route('/sitemap')
def sitemap():
    return redirect(url_for('static',filename='sitemap.xml'))


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Setting variables to be called in the base template
# Ideal color #1894EB; color generated to be used by navbar
@app.context_processor
def generate_random_color():
    r = lambda: randint(0,50)
    g = lambda: randint(100,180)
    b = lambda: randint(180,220)
    color = '#%02X%02X%02X' % (r(),g(),b()) #string formatting used where 02 represents 2 values and padded by 0, X to return hex
    return dict(generated_color=color)
