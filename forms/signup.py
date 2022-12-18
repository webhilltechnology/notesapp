from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired,EqualTo


class Signup(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    user_name = StringField('User Name', validators=[DataRequired()])
    email = EmailField('Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',message="Given Password is mismatching")])
    submit = SubmitField('Sing Up')
