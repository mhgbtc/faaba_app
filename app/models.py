import os
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
import json
import datetime
from time import time
import jwt
from flask_login import UserMixin

database_name = 'faaba_db'
# database_path = "postgresql://faaba_db:gUyG4OesFjXMgv2O5Id0bnkiTfKJPuIq@dpg-cg2dijg2qv24hdl141gg-a.frankfurt-postgres.render.com/faaba_db"
database_path = "postgresql://{}:{}@{}/{}".format("postgres", "root", "localhost:5432", database_name)
db = SQLAlchemy()

# setup_db() : binds a flask app and a SQLAlchemy service
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    
#----------------------------------------------------------------------------#
# User Model
#----------------------------------------------------------------------------#
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False, unique=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_driver = db.Column(db.Boolean, default=True)
    is_email_verified = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    
    # firstname = db.Column(db.String(255), nullable=False)
    # lastname = db.Column(db.String(255), nullable=False)
    # sexe = db.Column(db.String(2), nullable=True)
    # city = db.Column(db.String(255), nullable=True)
    # birthday = db.Column(db.DateTime, nullable=True)
    # phone = db.Column(db.String(12), nullable=False)
    # is_phone_visible = db.Column(db.Boolean, nullable=True, default=False)
    # is_driver = db.Column(db.Boolean, default=False)
    # profile_image = db.Column(db.String(255), nullable=True)
    # created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    # modified_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    
    # messages = db.relationship('Message', backref='user', lazy=True)
    # avis = db.relationship('Avis', backref='user', lazy=True)
    
    rides = db.relationship('Ride', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    
    def __init__(self, fullname, email, password, is_driver):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.is_driver = is_driver
        
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
            'fullname' : self.fullname,
            'email' : self.email,
            'password' : self.password,
            'is_driver' : self.is_driver,
            'is_email_verified' : self.is_email_verified,
            'registration_date' : self.registration_date
        }
    
#----------------------------------------------------------------------------#
# Ride Model
#----------------------------------------------------------------------------#
class Ride(db.Model):
    __tablename__ = 'rides'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    departure = db.Column(db.String(255), nullable=False)
    arrival = db.Column(db.String(255), nullable=False)
    boardingLocation = db.Column(db.String(255), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    estimated_arrival_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    seats = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    
    bookings = db.relationship('Booking', backref='ride', lazy=True)
    
    def __init__(self, driver_id, departure, arrival, boardingLocation, departure_date, estimated_arrival_date, seats, price):
        self.driver_id = driver_id
        self.departure = departure
        self.arrival = arrival
        self.boardingLocation = boardingLocation
        self.departure_date = departure_date
        self.estimated_arrival_date = estimated_arrival_date
        self.seats = seats
        self.price = price
        
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
            'driver_id' : self.driver_id,
            'departure' : self.departure,
            'boardingLocation' : self.boardingLocation,
            'arrival' : self.arrival,
            'departure_date' : self.departure_date,
            'estimated_arrival_date' : self.estimated_arrival_date,
            'seats' : self.seats,
            'price' : self.price
        }
    
#----------------------------------------------------------------------------#
# Booking Model
#----------------------------------------------------------------------------#
class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    
    def __init__(self, passenger_id, ride_id):
        self.passenger_id = passenger_id
        self.ride_id = ride_id
    
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
            'passenger_id' : self.passenger_id,
            'ride_id' : self.ride_id
        }
        
#----------------------------------------------------------------------------#
# Message Model
#----------------------------------------------------------------------------#
# class Message(db.Model):
#     __tablename__ = 'messages'
    
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     receiver = db.Column(db.String(255), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     sended_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
#     edited_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    
#     def __init__(self, user_id, receiver, content):
#         self.user_id = user_id
#         self.receiver = receiver
#         self.content = content
        
#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
    
#     def format(self):
#         return{
#             'id' : self.id,
#             'user_id' : self.user_id,
#             'receiver' : self.receiver,
#             'content' : self.content,
#             'sended_at' : self.sended_at,
#             'edited_at' : self.edited_at
#         }
    
#----------------------------------------------------------------------------#
# Avis Model
#----------------------------------------------------------------------------#
# class Avis(db.Model):
#     __tablename__ = 'avis'
    
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     receiver = db.Column(db.String(255), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(timezone('Africa/Porto-Novo')))
    
#     def __init__(self, user_id, receiver, content):
#         self.user_id = user_id
#         self.receiver = receiver
#         self.content = content
        
#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
    
#     def format(self):
#         return{
#             'id' : self.id,
#             'user_id' : self.user_id,
#             'receiver' : self.receiver,
#             'content' : self.content,
#             'date' : self.date
#         }
    
#----------------------------------------------------------------------------#
# Car Model
#----------------------------------------------------------------------------#
# class Car(db.Model):
#     __tablename__ = 'cars'
    
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     mark = db.Column(db.String(255), nullable=False)
#     model = db.Column(db.String(255), nullable=False)
#     year = db.Column(db.Integer, nullable=False)
#     color = db.Column(db.String(255), nullable=False)
#     mileage = db.Column(db.Integer, nullable=False)
    
#     def __init__(self, user_id, mark, model, year, color, mileage):
#         self.user_id = user_id
#         self.mark = mark
#         self.model = model
#         self.year = year
#         self.color = color
#         self.mileage = mileage
    
#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
    
#     def format(self):
#         return{
#             'id' : self.id,
#             'user_id' : self.user_id,
#             'mark' : self.mark,
#             'model' : self.model,
#             'year' : self.year,
#             'color' : self.color,
#             'mileage' : self.mileage,
#         }