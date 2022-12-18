from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

"""def create_app():
    app = Flask(__name__)
    with app.app_context():
        db.create_all()
    return app"""

app = Flask(__name__)


app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
#old SQL 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
#NEW SQL DB 

#print('Secret_key:'+os.environ.get('DB_URL'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



db = SQLAlchemy()
db.init_app(app)

mail = Mail(app)

migrate = Migrate(app, db, render_as_batch=True)


