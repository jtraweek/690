import flask_login
import flask_sqlalchemy
import sqlalchemy.ext.hybrid

from app import db, crypt




########################################################################
#   Relationship table to link users and their trips
user_trips = db.Table('user_trips',
            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
            db.Column('trip_id', db.Integer, db.ForeignKey('trip.trip_id')))




########################################################################
#   User database definitions
#
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
    ###
    def is_active(self):
        return True
    ###
    def get_id(self):
        return self.id




########################################################################
#   Trip database definitions
#
class Trip(db.Model):
    __tablename__ = 'trip'
    trip_id  = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String)
    location = db.Column(db.String)
    about    = db.Column(db.String)
    length   = db.Column(db.Integer)
    complete = db.Column(db.Boolean)
    itinerary_image = db.Column(db.String) # The image for the trip that will
                                           # appear on the itineraries page.
                                           # Expected to be located in
                                           # static/img/.
    users    = db.relationship('User',
                                secondary=user_trips,
                                backref=db.backref('trips', lazy='dynamic'))

    def __repr__(self):
        return "Trip %s" % self.title

    def mark_complete(self):
        self.complete = True

    def invite(self, user):
        if user not in self.users:
            self.users.append(user)

    def get_sorted_activities(self):
        """ Returns the activities of a trip, sorted by date.
        """
        activities = self.activities
        if activities:
            sorted_activities = sorted(activities, key=lambda act: act.length)
            return sorted_activities
        else:
            return []



########################################################################
#   Activity database definitions
#
class Activity(db.Model):
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



########################################################################
#   Store filepaths to photo files for a trip.
#
class TripPhoto(db.Model):
    __tablename__ = 'trip_photo'
    id          = db.Column(db.Integer,  primary_key=True)
    filepath    = db.Column(db.String)
    trip_id     = db.Column(db.Integer, db.ForeignKey('trip.trip_id'))
    trip        = db.relationship("Trip", backref="photos")

    def __repr__(self):
        return "TripPhoto %s" % self.filepath
