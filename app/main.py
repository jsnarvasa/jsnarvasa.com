from flask import Flask, render_template, send_from_directory
from os import listdir

# the all-important app variable:
app = Flask(__name__)

@app.route("/")
def index():
    image_names = listdir('./static/images')
    return render_template("index.html", image_names=image_names)

@app.route("/send_image/<filename>")
def send_image(filename):
    return send_from_directory("static/images", filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
