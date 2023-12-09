from . import db #access the package i am already in
from flask_login import UserMixin
from sqlalchemy.sql import func



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #stores real time data
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#use the same convention for other tables

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) #each user has their own email
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    notes = db.relationship('Note') #relationship is in caps
    user_translations = db.relationship('User_Translation')

class User_Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(10000))
    translated_text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #stores real time data
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(10000))
    translated_text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #stores real time data

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    subject = db.Column(db.String(150))
    message = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #stores real time data



