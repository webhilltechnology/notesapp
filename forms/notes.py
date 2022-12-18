from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class Note(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    note = TextAreaField('Notes', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Add Notes')
