from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from flask_wtf.file import FileRequired


class Upload(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Upload')
