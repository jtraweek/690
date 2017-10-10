import app.models           as models

from flask_wtf              import FlaskForm
from flask_wtf.file         import (FileField, FileRequired, FileAllowed)
from wtforms                import (StringField, IntegerField, TextAreaField,
                                    PasswordField, BooleanField,
                                    SubmitField)
from wtforms.validators     import (DataRequired, Email)

from app import uploaded_photos


class SigninForm(FlaskForm):
    username    = StringField('Username', validators=[DataRequired()])
    password    = PasswordField('Password', validators=[DataRequired()])
    _found_user = None

    @property
    def found_user(self):
        return self._found_user

    def validate(self):
        if FlaskForm.validate(self):
            lookup = models.User.query.filter_by(username=self.username.data).first()
            if lookup and lookup.password_matches(self.password.data):
                self._found_user = lookup
                return True
            else:
                self._found_user = None
                self.password.errors.append('Invalid username or password')
                return False
        else:
            return False


class RegisterForm(FlaskForm):
    username    = StringField('Username', validators=[DataRequired()])
    email       = StringField('Email', validators=[DataRequired(), Email()])
    password    = PasswordField('Password', validators=[DataRequired()])

    def validate(self):
        if FlaskForm.validate(self):
            lookup = models.User.query.filter_by(username=self.username.data).first()
            if lookup:
                self.username.errors.append('Username already taken')
                return False
            else:
                return True
        else:
            return False


class NewTripForm(FlaskForm):
    title    = StringField('Trip Name', validators=[DataRequired()])
    location = StringField('Location')
    about    = TextAreaField('Care to Show any Focus?')
    length   = IntegerField('Number of Days')
    complete = BooleanField('This Trip is Complete!')


class NewActivityForm(FlaskForm):
    title = StringField('activity_title', validators=[DataRequired()])
    location = StringField('activity_location')
    length = StringField('activity_length', validators=[DataRequired()])
    description = TextAreaField('activity_description')


class SearchLocationForm(FlaskForm):
    location_search = StringField('Search Locations')


class TripPhotoUploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(uploaded_photos, u'Must be an image file!'),
                                    FileRequired(u'File required!')])
    submit = SubmitField(u'Upload')
