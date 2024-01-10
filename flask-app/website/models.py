from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    user_added_translation = db.relationship('User_Added_Translation') #store the different translations added ids made by the user
    user_translation = db.relationship('User_Translation') #store the different translation requests

class Subscribe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    other_email = db.Column(db.String(150))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    subject = db.Column(db.String(150))
    message = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #stores real time data

class User_Added_Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(10000))
    translated_text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User_Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(10000))
    translated_text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(10000))
    translated_text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #stores real time data

