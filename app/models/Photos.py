from app import db

class Photos(db.Model):
    __tablename__ = 'Photos'

    PhotoID = db.Column('PhotoID',db.Integer, primary_key=True, autoincrement=True)
    FileName = db.Column('FileName', db.String(100), nullable=False, unique=True)
    Caption = db.Column('Caption', db.String(5000))
    Upload_Date = db.Column('Upload_Date', db.Date, nullable=False)
    Capture_Date = db.Column('Capture_Date', db.Date)
    Place = db.Column('Place', db.String(150))
    City = db.Column('City', db.String(150))
    Country = db.Column('Country', db.String(150))


    @classmethod
    def get_photo_list(cls, currentPage=1, perPage=9):
        currentPage = int(currentPage)
        return cls.query.order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items

    @classmethod
    def search_photo_list(cls, searchQuery, currentPage=1, perPage=9):
        currentPage = int(currentPage)
        return cls.query.filter((Photos.Country.like('%' + searchQuery + '%')) | (Photos.City.like('%' + searchQuery + '%')) | (Photos.Place.like('%' + searchQuery + '%'))).order_by(Photos.Capture_Date.desc()).paginate(page=currentPage, per_page=perPage, error_out=False).items
        