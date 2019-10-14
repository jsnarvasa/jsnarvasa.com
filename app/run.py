import socket
from app import app, db
import config

hostname = socket.gethostname()

if __name__ == "__main__":
    db.create_all()
    if hostname == config.hostname['PROD']:
        app.run(host='localhost', port=80, debug=False)
    else:
        app.run(host='localhost', port=80, debug=True)
