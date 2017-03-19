from flask_wtf              import FlaskForm
from wtforms                import StringField, IntegerField, TextAreaField
from wtforms.validators     import DataRequired
from wtforms.widgets        import TextArea

class NewTripForm(FlaskForm):
    title    = StringField('title', validators=[DataRequired()])
    location = StringField('location')
    about    = TextAreaField('about')
    length   = IntegerField('length')
