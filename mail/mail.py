from app import mail
from flask_mail import Message

WELCOME_MSG = "Hi Welcome to Notes App...! " \
              "Here your all notes will saved in cloud with safe way..." \
              "Happy Notes day...!"

def welcome(user_email):
    print(type(user_email))
    msg = Message("Welcome to Notes App", recipients=[user_email])
    msg.body = WELCOME_MSG
    mail.send(msg)
    print("sent")

