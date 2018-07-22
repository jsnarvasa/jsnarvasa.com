from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime
from models import model
import yaml


app = Flask(__name__)


# Configure Database
db = yaml.load(open('database_config.yaml'))
mysql_user = db["mysql_user"]
mysql_password = db["mysql_password"]
mysql_host = db["mysql_host"]
mysql_db = db["mysql_db"]
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://" + mysql_user + ":" + mysql_password + "@" + mysql_host + "/" + mysql_db + "?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
model.db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gallery")
def gallery():
    image_names = model.Photos.query.order_by(model.Photos.PhotoID.asc()).limit(30) #set to 9 after pagination implemented
    return render_template("gallery.html", image_names=image_names)


@app.route("/getphotodetails")
def getphotodetails():
    filename = request.args.get('img', 'Error', type=str)
    image = model.Photos.query.filter_by(FileName=filename).first()
    Caption = image.Caption
    City = image.City
    Country = image.Country
    Upload_Date = image.Upload_Date.strftime("%A, %d %B %Y")
    Capture_Date = image.Capture_Date.strftime("%A, %d %B %Y")
    return jsonify(Caption=Caption, City=City, Country=Country,Upload_Date=str(Upload_Date), Capture_Date=str(Capture_Date))


@app.route("/photo/<photo>")
def photo_view(photo):
    return render_template("photo.html", photo=photo)


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
