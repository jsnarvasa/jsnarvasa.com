import socket
from app import app, db
import config

hostname = socket.gethostname()

if __name__ == "__main__":
    db.create_all()
    if hostname == config.hostname['PROD']:
        app.run(port=6000, debug=True)
    else:
        app.run(host='localhost', port=5000, debug=True)
