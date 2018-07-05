from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Photos(db.Model):
    __tablename__ = 'photos'
    PhotoID = db.Column('PhotoID',db.Integer, primary_key = True)
    FileName = db.Column('FileName', db.String(30))
    Title = db.Column('Title', db.String(150))
    Description = db.Column('Description', db.String(500))
    Upload_Date = db.Column('Upload_Date', db.Date)
    Capture_Date = db.Column('Capture_Date', db.Date)

    def __repr__(self):
        return '<Photos %r>' % self.FileName