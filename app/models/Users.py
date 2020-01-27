from app import db, flask_bcrypt


class Users(db.Model):
    __tablename__ = 'Users'

    Username = db.Column('Username', db.String(100), primary_key=True)
    Password = db.Column('Password', db.String(255), nullable=False)

    @classmethod
    def get_password_hash(cls, username):
        return cls.query.filter(cls.Username == username).first().Password