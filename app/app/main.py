from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from random import randint
from models import model
import yaml


app = Flask(__name__)


# Configure Database
db = yaml.load(open('database_config.yaml'))
mysql_user = db["mysql_user"]
mysql_password = db["mysql_password"]
mysql_host = db["mysql_host"]
mysql_db = db["mysql_db"]
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + mysql_user + ":" + mysql_password + "@" + mysql_host + "/" + mysql_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gallery")
def gallery():
    image_names = model.Photos.query.all()
    return render_template("gallery.html", image_names=image_names)


@app.route("/getphotodetails")
def getphotodetails():
    result = request.args.get('a', 0, type=str)
    return jsonify(result=result)


@app.route("/photo/<photo>")
def photo_view(photo):
    return render_template("photo.html", photo=photo)


# Setting variables to be called in the base template
# Ideal color #1894EB; color generated to be used by navbar
@app.context_processor
def generate_random_color():
    r = lambda: randint(0,50)
    g = lambda: randint(100,180)
    b = lambda: randint(180,220)
    color = '#%02X%02X%02X' % (r(),g(),b())
    return dict(generated_color=color)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
