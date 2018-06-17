from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Photos(db.Model):
    __tablename__ = 'photos'
    PhotoID = db.Column('PhotoID',db.Integer, primary_key = True)
    FileName = db.Column('FileName', db.String(30))

    def __repr__(self):
        return '<Photos %r>' % self.FileName