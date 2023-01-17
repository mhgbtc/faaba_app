import os
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
import json
import datetime

database_name = 'faabadb'
database_path = "postgresql://{}:{}@{}/{}".format("postgres", "root", "localhost:5432", database_name)
db = SQLAlchemy()

# setup_db() : binds a flask app and a SQLAlchemy service
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    
#----------------------------------------------------------------------------#
# User Model
#----------------------------------------------------------------------------#
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    sexe = db.Column(db.String(2), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)
    phone = db.Column(db.String(12), nullable=False)
    is_phone_visible = db.Column(db.Boolean, nullable=True, default=False)
    is_driver = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    
    messages = db.relationship('Message', backref='user', lazy=True)
    avis = db.relationship('Avis', backref='user', lazy=True)
    trajets = db.relationship('Trajet', backref='user', lazy=True)
    reservations = db.relationship('Reservation', backref='user', lazy=True)
    
    def __init__(self, firstname, lastname, email, password, phone):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phone = phone
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
            'id' : self.id,
            'firstname' : self.firstname,
            'lastname' : self.lastname,
            'email' : self.email,
            'password' : self.password,
            'sexe' : self.sexe,
            'city' : self.city,
            'birthday' : self.birthday,
            'phone' : self.phone,
            'is_phone_visible' : self.is_phone_visible,
            'is_driver' : self.is_driver,
            'profile_image' : self.profile_image,
            'created_at' : self.created_at
        }
    
#----------------------------------------------------------------------------#
# Message Model
#----------------------------------------------------------------------------#
class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sended_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    edited_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    
    def __init__(self, user_id, receiver, content):
        self.user_id = user_id
        self.receiver = receiver
        self.content = content
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
            'id' : self.id,
            'user_id' : self.user_id,
            'receiver' : self.receiver,
            'content' : self.content,
            'sended_at' : self.sended_at,
            'edited_at' : self.edited_at
        }
    
#----------------------------------------------------------------------------#
# Avis Model
#----------------------------------------------------------------------------#
class Avis(db.Model):
    __tablename__ = 'avis'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    
    def __init__(self, user_id, receiver, content):
        self.user_id = user_id
        self.receiver = receiver
        self.content = content
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
            'id' : self.id,
            'user_id' : self.user_id,
            'receiver' : self.receiver,
            'content' : self.content,
            'date' : self.date
        }
    
#----------------------------------------------------------------------------#
# Trajet Model
#----------------------------------------------------------------------------#
class Trajet(db.Model):
    __tablename__ = 'trajets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_location = db.Column(db.String(255), nullable=False)
    destination_location = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    start_hour = db.Column(db.String(50), nullable=False)
    participation = db.Column(db.Float, nullable=True)
    is_regular = db.Column(db.Boolean, default=False)
    nbr_places = db.Column(db.Integer, nullable=False, default=1)
    reservations = db.relationship('Reservation', backref='trajet', lazy=True)
    
    def __init__(self, user_id, start_location, destination_location, start_date, start_hour, participation, is_regular, nbr_places):
        self.user_id = user_id
        self.start_location = start_location
        self.destination_location = destination_location
        self.start_date = start_date
        self.start_hour = start_hour
        self.participation = participation
        self.is_regular = is_regular
        self.nbr_places = nbr_places
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
            'id' : self.id,
            'user_id' : self.user_id,
            'start_location' : self.start_location,
            'destination_location' : self.destination_location,
            'start_date' : self.start_date,
            'start_hour' : self.start_hour,
            'participation' : self.participation,
            'is_regular' : self.is_regular,
            'nbr_places' : self.nbr_places
        }
    
#----------------------------------------------------------------------------#
# Reservation Model
#----------------------------------------------------------------------------#
class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trajet_id = db.Column(db.Integer, db.ForeignKey('trajets.id'), nullable=False)
    nbr_places_res = db.Column(db.Integer, nullable=False, default=1)
    
    def __init__(self, user_id, trajet_id, nbr_places_res):
        self.user_id = user_id
        self.trajet_id = trajet_id
        self.nbr_places_res = nbr_places_res
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
            'id' : self.id,
            'user_id' : self.user_id,
            'trajet_id' : self.trajet_id,
            'nbr_places_res' : self.nbr_places_res
        }
    
#----------------------------------------------------------------------------#
# Car Model
#----------------------------------------------------------------------------#
class Car(db.Model):
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mark = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(255), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    
    def __init__(self, user_id, mark, model, year, color, mileage):
        self.user_id = user_id
        self.mark = mark
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
            'id' : self.id,
            'user_id' : self.user_id,
            'mark' : self.mark,
            'model' : self.model,
            'year' : self.year,
            'color' : self.color,
            'mileage' : self.mileage,
        }