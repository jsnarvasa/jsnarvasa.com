import socket
from app import app, db
import config

hostname = socket.gethostname()
db.create_all()

if __name__ == "__main__":
    if hostname == config.hostname['PROD']:
        app.run(port=6000)
    else:
        app.run(host='localhost', port=5000, debug=True)
