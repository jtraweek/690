import app.models           as models

from flask_wtf              import FlaskForm
from wtforms                import (StringField, IntegerField, TextAreaField,
                                    PasswordField)
from wtforms.validators     import (DataRequired, Email)



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
    title    = StringField('title', validators=[DataRequired()])
    location = StringField('location')
    about    = TextAreaField('about')
    length   = IntegerField('length')

class NewActivityForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    location = StringField('location')
    description = TextAreaField('description')
    length = IntegerField('length')