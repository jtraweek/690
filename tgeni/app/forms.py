from flask_wtf              import Form
from wtforms                import StringField, IntegerField
from wtforms.validators     import DataRequired
from wtforms.widgets        import TextArea

class NewTripForm(Form):
    title = StringField('title', validators=[DataRequired()])
    length= IntegerField('length')
    about = StringField('about', widget=TextArea())
