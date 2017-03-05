import flask_login
import sqlalchemy.ext.hybrid

from app import db, crypt

class User(db.Model, flask_login.UserMixin):

    """ User database model
        Class to hold database records for registered users. This class
        handles password hashing and login functionality.
    """
    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String,  unique=True)
    email     = db.Column(db.String,  unique=True)
    _password = db.Column(db.String(128)) # hashed

    def __repr__(self):
        return '<User %r>' % (self.username)

    # functionality to hash passwords
    @sqlalchemy.ext.hybrid.hybrid_property
    def password(self):
        return self._password
    @password.setter
    def _set_password(self, plaintext_password):
        self._password = crypt.generate_password_hash(plaintext_password)

    def password_matches(self, plaintext_password):
        return crypt.check_password_hash(self._password, plaintext_password)

    # required methods for flask_login...
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id
        
class Trip(db.Model):
    trip_id = db.Column(db.Integer, primary_key=True)
    trip_name = db.Column(db.String)
    trip_length = db.Column(db.Integer)
    
    def __init__(self, trip_name, trip_length):
        self.trip_name = trip_name
        self.trip_length = trip_length
        
    def __repr__(self):
        return "User %s" % self.trip_name
