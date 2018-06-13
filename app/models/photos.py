from main import db


class Photos(db.Model):
    __tablename__ = 'photos'
    PhotoID = db.Column('PhotoID',db.Integer, primary_key = True)
    FileName = db.Column('FileName', db.Unicode)

    def __repr__(self):
        return '<Photos %r>' % self.FileName