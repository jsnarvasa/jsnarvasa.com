from app import db, flask_bcrypt


class Users(db.Model):
    """Contains the data and methods necessary to manage users within the Photoblog component"""

    __tablename__ = 'Users'

    Username = db.Column('Username', db.String(100), primary_key=True)
    Password = db.Column('Password', db.String(255), nullable=False)

    @classmethod
    def get_password_hash(cls, username):
        """Obtains password hash of the given user"""
        return cls.query.filter(cls.Username == username).first().Password