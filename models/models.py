from app import db
from flask_login import UserMixin
from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250))
    user_name = db.Column(db.String(250))
    password = db.Column(db.String(250))
    email = db.Column(db.String(250))
    created_date = db.Column(db.DateTime, default=datetime.now(IST))

    notes = db.relationship('Notes',backref='note')

    def __repr__(self):
        return self.user_name

class Notes(db.Model, UserMixin):
    notes_id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(250))
    notes = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.now(IST))
    last_updated_date = db.Column(db.DateTime, default=datetime.now(IST))

    #Foregin Key
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __repr__(self):
        return self.title

