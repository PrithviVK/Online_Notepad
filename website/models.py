from . import db  #equivalent to from website import db
from flask_login import UserMixin #usermixin is used to access the current_user object in auth.py 
#that holds all info about the user
from sqlalchemy.sql import func


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)#unique mail id
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    notes=db.relationship('Note')#'Note class' relationship with user to store all notes of the user


class Note(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True),default=func.now())#func is used to get current date automatically
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))#user.id(is in lower case) in User model
    #is been referenced by user_id in Note since every note is owned by someone
    
