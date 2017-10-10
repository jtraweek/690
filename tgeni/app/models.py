import app.utils.helpers as helpers
import flask_login
import flask_sqlalchemy
import sqlalchemy.ext.hybrid

from app import db, crypt


class CRUDMixin(object):
    """ Provides a base class with methods used by every model. This
        automates much of the database session management.
    """
    __table_args__ = { 'extend_existing': True }

    # TODO: Create an ID field shared by all models?

    @classmethod
    def create(cls, commit=True, **kwargs):
        """ Create a new object in the database. 'commit' indicates whether
            to commit the change right away (if not it will need to be saved
            later).
            Returns the new object.
            This is a static method.
        """
        obj = cls(**kwargs)
        return obj.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(int(id))

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, commit=True, **kwargs):
        """
        """
        for (attr, val) in kwargs.items():
            setattr(self, attr, val)
        return self.save(commit=commit)

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(int(id))


#   Relationship table to link users and their trips
user_trips = db.Table('user_trips',
            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
            db.Column('trip_id', db.Integer, db.ForeignKey('trip.trip_id')))


class User(db.Model, flask_login.UserMixin, CRUDMixin):
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
    ###
    def is_active(self):
        return True
    ###
    def get_id(self):
        return self.id


class Trip(db.Model, CRUDMixin):
    __tablename__ = 'trip'
    trip_id  = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String)
    location = db.Column(db.String)
    about    = db.Column(db.String)
    length   = db.Column(db.Integer)
    complete = db.Column(db.Boolean)
    icon     = db.Column(db.String) # The image for the trip that will
                                           # appear on the itineraries page.
                                           # Expected to be located in
                                           # static/img/.
    number_of_likes=db.Column(db.integer,default=0)
    users    = db.relationship('User',
                                secondary=user_trips,
                                backref=db.backref('trips', lazy='dynamic'))

    def __repr__(self):
        return "Trip %s" % self.title

    def mark_complete(self):
        self.complete = True

    def invite(self, *invitees):
        for user in invitees:
            if user not in self.users:
                self.users.append(user)

    def get_sorted_activities(self):
        """ Returns the activities of a trip, sorted by date.
        """
        return helpers.get_sorted_activities(self)

    def add_number_of_Likes(self):
        self.number_of_likes+1
        
    def get_number_of_likes(self):
        return self.number_of_likes
    
class Activity(db.Model, CRUDMixin):
    __tablename__ = 'activity'
    activity_id = db.Column(db.Integer,  primary_key=True)
    title       = db.Column(db.String, nullable=True)
    location    = db.Column(db.String, nullable=True)
    length      = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    trip_id     = db.Column(db.Integer, db.ForeignKey('trip.trip_id'))
    trip        = db.relationship("Trip", backref="activities")

    def __repr__(self):
        return "Activity %s" % self.title


class TripPhoto(db.Model, CRUDMixin):
    __tablename__ = 'trip_photo'
    id          = db.Column(db.Integer,  primary_key=True)
    filepath    = db.Column(db.String)
    trip_id     = db.Column(db.Integer, db.ForeignKey('trip.trip_id'))
    trip        = db.relationship("Trip", backref="photos")

    def __repr__(self):
        return "TripPhoto %s" % self.filepath
