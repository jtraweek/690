from flask_login    import UserMixin
from app            import db


class User(db.Model, UserMixin):
    id       = db.Column(db.Integer,    primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email    = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))

    def __init__(self, username, email, password):
        self.username = username
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

    # required methods for flask_login...

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

