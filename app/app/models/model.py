from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Photos(db.Model):
    __tablename__ = 'Photos'
    PhotoID = db.Column('PhotoID',db.Integer, primary_key = True)
    FileName = db.Column('FileName', db.String(100))
    Caption = db.Column('Caption', db.String(5000))
    Upload_Date = db.Column('Upload_Date', db.Date)
    Capture_Date = db.Column('Capture_Date', db.Date)
    Place = db.Column('Place', db.String(150))
    City = db.Column('City', db.String(150))
    Country = db.Column('Country', db.String(150))
    