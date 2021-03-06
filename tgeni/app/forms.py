
import app.models as models

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import BooleanField, IntegerField, PasswordField, \
                        StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

from app import uploaded_photos
from app.validators import ExtensionAllowed


class SigninForm(FlaskForm):
    username    = StringField('Username', validators=[DataRequired()])
    password    = PasswordField('Password', validators=[DataRequired()])
    _found_user = None

    @property
    def found_user(self):
        return self._found_user

    def validate(self):
        if FlaskForm.validate(self):
            lookup = models.User.get_by_username(self.username.data)
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
            lookup = models.User.get_by_username(self.username.data)
            if lookup:
                self.username.errors.append('Username already taken')
                return False
            else:
                return True
        else:
            return False


class UpdateProfileForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email', validators=[Email()])
    bio = TextAreaField('Bio')
    avatar = FileField('Avatar',
        validators=[
            Optional(),
            ExtensionAllowed(uploaded_photos, u'Must be an image file!')
            ],
        )


class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password',
                                validators=[DataRequired()])
    confirm  = PasswordField('Confirm New Password',
                                validators=[
                                    DataRequired(),
                                    EqualTo('password', message='Passwords must match')
                                ])


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
    photo = FileField(
                validators=[
                    FileRequired(u'File required!'),
                    ExtensionAllowed(uploaded_photos, u'Must be an image file!'),
                    ]
                )
    submit = SubmitField(u'Upload')
