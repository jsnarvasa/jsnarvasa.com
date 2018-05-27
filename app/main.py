from flask import Flask, render_template, send_from_directory
from os import listdir
from flask_mysqldb import MySQL
import yaml

# the all-important app variable:
app = Flask(__name__)

# Configure Database
db = yaml.load(open('database_config.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route("/")
def index():
    image_names = listdir('./static/images')
    return render_template("index.html", image_names=image_names)

@app.route("/send_image/<filename>")
def send_image(filename):
    return send_from_directory("static/images", filename)

if __name__ == "__main__":
    #app.run(host='0.0.0.0', debug=True, port=80)
    app.run()
