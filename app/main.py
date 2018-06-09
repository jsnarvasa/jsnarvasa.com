from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import yaml


# the all-important app variable:
app = Flask(__name__)


# Configure Database
db = yaml.load(open('database_config.yaml'))
mysql_user = db["mysql_user"]
mysql_password = db["mysql_password"]
mysql_host = db["mysql_host"]
mysql_db = db["mysql_db"]
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + mysql_user + ":" + mysql_password + "@" + mysql_host + "/" + mysql_db
db = SQLAlchemy(app)


class Photos(db.Model):
    __tablename__ = 'photos'
    PhotoID = db.Column('PhotoID',db.Integer, primary_key = True)
    FileName = db.Column('FileName', db.Unicode)

    def __repr__(self):
        return '<Photos %r>' % self.FileName


@app.route("/")
def index():
    image_names = Photos.query.all()
    return render_template("index.html", image_names=image_names)


@app.route("/send_image/<filename>")
def send_image(filename):
    return send_from_directory("static/images/", filename)


if __name__ == "__main__":
    app.run(debug=True)
