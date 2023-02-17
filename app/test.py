import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *

class FaabaTestCase(unittest.TestCase):
    # This class represents the faaba test case.

    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "faaba_db_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','root','localhost:5432', self.database_name)
        with self.app.app_context():
            setup_db(self.app, self.database_path)
            
        self.headers = {'Authorization': 'Bearer ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjo0LCJleHBpcmF0aW9uIjoiMjAyMy0wMi0xNiAyMTo1Njo1Mi4zMzg1NDYifQ.k1OKZ1wicW1c9HTaoqpXTF_gmmsgkDPYhcd8quPC-uU'}
        
        self.new_user = {
            "email" : "samtest7@gmail.com",
            "password" : "Test1234",
            "confirm_password" : "Test1234"
        }
        
        self.new_invalid_user = {
            "email" : "samtest",
            "password" : "Test1234",
            "confirm_password" : "Test1234"
        }
        
        self.log_valid_user = {
            "email" : "samtest1@gmail.com",
            "password" : "Test1234"
        }
        
        self.log_invalid_user = {
            "email" : "samtest1@gmail.com",
            "password" : "test1234500"
        }
         
        self.update_user = {
            "firstname" : "Samuel",
            "lastname" : "Babarou",
            "email" : "badiou2@gmail.com",
            "password" : "badioucom",
            "phone" : "+22995648125",
            "sexe" : "M",
            "is_driver" : True
        }
        
        self.update_invalid_user = {
            "firstname" : "Samu",
            "lastname" : "Baba",
            "email" : "badiou",
            "phone" : "+22995648125",
            "sexe" : "M",
            "is_driver" : True
        }
        
        self.new_valid_car = {
            "user_id" : 23,
            "mark" : "BMW",
            "model" : "B103400",
            "year" : 2022,
            "color" : "red",
            "mileage" : 1200,
        }
        
        self.new_invalid_car = {
            "mark" : "BMW",
            "year" : 2022,
            "color" : "red",
            "mileage" : 1200,
        }
        
        self.update_valid_car = {
            "user_id" : 23,
            "mark" : "Toyota",
            "model" : "100-3030",
            "year" : 1999,
            "color" : "red",
            "mileage" : 1200,
        }
        
        self.update_invalid_car = {
            "user_id" : 23,
            "model" : "100-3030",
            "year" : 1999,
            "color" : "red",
            "mileage" : 1200,
        }
        
        self.new_valid_ride = {
            'driver_id' : 4,
            'departure' : "Porto-Novo",
            'arrival' : "Parakou",
            "departure_date" : "03-02-2023 12:00",
            'estimated_arrival_date' : "10-02-2023 16:00",
            'seats' : 2  
        }
        
        self.new_invalid_ride = {
            'driver_id' : 1,
            'departure' : "Porto-Novo",
            'arrival' : "Cotonou",
            'estimated_arrival_date' : "06-01-2023 12:00",
            'seats' : 0    
        }
        
        self.update_valid_ride = {
            'driver_id' : 1,
            'departure' : "Porto-Novo",
            'arrival' : "Calavi",
            "departure_date" : "03-02-2023 20:00",
            'estimated_arrival_date' : "10-02-2023 16:00",
            'seats' : 4 
        }
        
        self.update_invalid_ride = {
            'driver_id' : 1,
            'departure' : "Porto-Novo",
            'arrival' : "Parakou",
            'estimated_arrival_date' : "06-01-2023 12:00",
            'seats' : 0    
        }
        
        self.new_valid_booking = {
            'passenger_id' : 5,
            'ride_id' : 9
        }
        
        self.new_invalid_booking = {
            'user_id' : 17,
            'nbr_places_res' : 3
        }
        
        self.update_valid_booking = {
            'passenger_id' : 4,
            'ride_id' : 9
        }
        
        self.update_invalid_booking = {
            'user_id' : 28,
            'nbr_places_res' : 5
        }
        
        self.new_valid_avis = {
            'user_id' : 17,
            'receiver' : "badiou2@gmail.com",
            'content' : "I am a good content for test"
        }
        
        self.new_invalid_avis = {
            'user_id' : 17,
            'receiver' : "badiou200@gmail.com",
            'content' : "I am a good content for test"
        }
        
        self.update_valid_avis = {
            'user_id' : 17,
            'receiver' : "badiou2@gmail.com",
            'content' : "Je suis un contenu de test"
        }
        
        self.update_invalid_avis = {
            'user_id' : 17,
            'receiver' : "badiou200@gmail.com",
            'content' : "I am a good content for test"
        }
        
        self.new_valid_message = {
            'user_id' : 17,
            'receiver' : "badiou2@gmail.com",
            'content' : "Message sent for test"
        }
        
        self.new_invalid_message = {
            'user_id' : 17,
            'receiver' : "badiou200@gmail.com",
            'content' : "Message not sent for test"
        }
        
        self.update_valid_message = {
            'user_id' : 17,
            'receiver' : "badiou2@gmail.com",
            'content' : "Je suis un message de test"
        }
        
        self.update_invalid_message = {
            'user_id' : 17,
            'receiver' : "badiou200@gmail.com",
            'content' : "I am a good content for test"
        }
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Writing at least one test for each test for successful operation and for expected errors.
    
    # #Testing new user insertion - Registration
    # def test_create_new_user(self):
    #     res = self.client().post("/register", json=self.new_user)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["created"])
        
    # #Testing a case user provid invalid inputs
    # def test_422_create_new_user(self):
    #     res = self.client().post("/register", json=self.new_invalid_user)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")
        
    # #Testing login valid user
    # def test_log_user(self):
    #     res = self.client().post("/login", json=self.log_valid_user)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["logged"])
        
    # #Testing login invalid user
    # def test_422_log_user(self):
    #     res = self.client().post("/login", json=self.log_invalid_user)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")
        
    # #Test create new ride
    # def test_create_ride(self):
    #     res = self.client().post('/rides', headers=self.headers, json=self.new_valid_ride)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    
    # #Test 422 create new ride
    # def test_422_create_ride(self):
    #     res = self.client().post('/rides', headers=self.headers, json=self.new_invalid_ride)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Testing when user attempt to create a ride but not connected
    # def test_401_create_ride(self):
    #     res = self.client().post('/rides', json=self.new_valid_ride)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 401)
        
    # #Test retrieve all rides
    # def test_get_rides(self):
    #     res = self.client().get('/rides')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['rides'])
        
    # #Test retrieve detail on existing unique ride
    # def test_get_ride_detail(self):
    #     res = self.client().get('/rides/2', headers=self.headers)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['ride'])
        
    # #Test 422 get detail on unexisting ride
    # def test_422_get_ride_detail(self):
    #     res = self.client().get('/rides/100', headers=self.headers)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # #Test 401 get detail on existing ride but not connected
    # def test_401_get_ride_detail(self):
    #     res = self.client().get('/rides/9')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 401)
        
    # # Test delete existing ride
    # def test_delete_ride(self):
    #     res = self.client().delete('/rides/14', headers=self.headers)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
        
    # #Test 422 delete unexisting ride
    # def test_422_delete_ride(self):
    #     res = self.client().delete('/rides/100', headers=self.headers)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test 401 on delete ride
    # def test_401_delete_ride(self):
    #     res = self.client().delete('/rides/13')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 401)
        
    # # Test update existing ride
    # def test_update_ride(self):
    #     res = self.client().put('/rides/10', headers=self.headers, json=self.update_valid_ride)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['updated'])
        
    # # Test 422 update unexisting ride
    # def test_422_update_ride(self):
    #     res = self.client().put('/rides/300', headers=self.headers, json=self.update_valid_ride)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test 422 update existing ride with invalid input
    # def test_422_update_invalid_ride(self):
    #     res = self.client().put('/rides/2', headers=self.headers, json=self.new_invalid_ride)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test 401 update existing ride
    # def test_401_update_ride(self):
    #     res = self.client().put('/rides/10', json=self.update_valid_ride)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 401)
    
    # # Test create new booking
    # def test_create_booking(self):
    #     res = self.client().post('/bookings', headers=self.headers, json=self.new_valid_booking)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
        
    # # Test 422 create new booking
    # def test_422_create_booking(self):
    #     res = self.client().post('/bookings', headers=self.headers, json=self.new_invalid_booking)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test 405 on create new booking
    # def test_405_create_booking(self):
    #     res = self.client().post('/bookings/100', headers=self.headers, json=self.new_valid_booking)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'method not allowed')
        
    # # Tes 401 create booking
    # def test_401_create_booking(self):
    #     res = self.client().post('/bookings', json=self.new_valid_booking)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 401)
        
    # # Test to retrieve all available bookings
    # def test_get_bookings(self):
    #     res = self.client().get('/bookings', headers=self.headers)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['bookings'])
        
    # def test_401_get_bookings(self):
    #     res = self.client().get('/bookings')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 401)
    
    # # Test get detail on single booking
    # def test_get_booking_detail(self):
    #     res = self.client().get('/bookings/1', headers=self.headers)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['booking'])
        
    # def test_401_get_booking_detail(self):
    #     res = self.client().get('/bookings/1')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 401)
        
    # # Test 422 retrieve infos on single unexisting booking
    # def test_422_get_booking_detail(self):
    #     res = self.client().get('/bookings/100', headers=self.headers)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test delete existing booking
    # def test_delete_booking(self):
    #     res = self.client().delete('/bookings/2', headers=self.headers)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
        
    # # Test 422 delete unexisting booking
    # def test_422_delete_booking(self):
    #     res = self.client().delete('/bookings/100', headers=self.headers)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test update booking
    # def test_update_booking(self):
    #     res = self.client().put('/bookings/1', headers=self.headers, json=self.update_valid_booking)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['updated'])
        
    # # Test 422 update existing booking with invalid inputs
    # def test_422_update_booking(self):
    #     res = self.client().put('/bookings/1', headers=self.headers, json=self.update_invalid_booking)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    
    # Test 401 update booking
    # def test_401_update_booking(self):
    #     res = self.client().put('/bookings/1', json=self.update_valid_booking)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 401)
    
    # =========================================================================END==================================================
        
    # #Testing retrieves users successfully
    # def test_get_users(self):
    #     res = self.client().get("/users")
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['users'])
        
    # #Testing error 422 when attempting to retrieve users
    # def test_422_get_users(self):
    #     res = self.client().get("/users/2")
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")
        
    # #Testing retrieve existing user detail
    # def test_get_user_detail(self):
    #     res = self.client().get('/users/17')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['user'])
        
    # #Testing deleting an existing user
    # def test_delete_user(self):
    #     res = self.client().delete('/users/29')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
        
    # #Testing deleting an unexisting user
    # def test_422_delete_user(self):
    #     res = self.client().delete('/users/1')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")
        
    # #Testing updating specific user who exists
    # def test_update_user(self):
    #     res = self.client().put('/users/32', json=self.update_user)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['updated'])
        
    # #Testing a case they attempt to update an unexisting user
    # def test_422_update_user(self):
    #     res = self.client().put('/users/12', json=self.update_user)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")
        
    # #Testing 422 error when update with anormal data
    # def test_422_update_user(self):
    #     res = self.client().put('/users/33', json=self.update_invalid_user)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")
    
    # #Test for successfully creating new car
    # def test_create_car(self):
    #     res = self.client().post('/cars', json=self.new_valid_car)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
        
    # #Test 422 create user
    # def test_422_create_car(self):
    #     res  = self.client().post('/cars', json=self.new_invalid_car)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    
    # #Test for successfully retrieving all cars
    # def test_get_cars(self):
    #     res = self.client().get('/cars')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['cars'])

    # #Test 422 not found cars
    # def test_422_get_cars(self):
    #     res = self.client().get('/cars/100')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "unprocessable")
        
    # #Test get car details
    # def test_get_car_detail(self):
    #     res = self.client().get('/cars/10')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['car'])
        
    # #Test delete car
    # def test_delete_car(self):
    #     res = self.client().delete('/cars/5')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
        
    # #Test 422 delete an unexisting car
    # def test_422_delete_car(self):
    #     res = self.client().delete('/cars/1')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # #Test update car
    # def test_update_car(self):
    #     res = self.client().put('/cars/11', json=self.update_valid_car)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['updated'])
        
    # #Test 422 update car : valid car but invalid user inputs
    # def test_422_update_car(self):
    #     res = self.client().put('/cars/11', json=self.update_invalid_car)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # #Test 422 not found car to update
    # def test_422_update_car(self):
    #     res = self.client().put('/cars/1', json=self.update_valid_car)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    
    # # Test create new avis
    # def test_create_avis(self):
    #     res = self.client().post('/avis', json=self.new_valid_avis)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
        
    # # Test 422 create new avis
    # def test_422_create_avis(self):
    #     res = self.client().post('/avis', json=self.new_invalid_avis)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test retrieve all avis
    # def test_get_avis(self):
    #     res = self.client().get('/avis')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['avis'])
        
    # # Test get unique avis detail
    # def test_get_avis_detail(self):
    #     res = self.client().get('/avis/1')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['avis'])
        
    # # Test fail get unexisting avis detail
    # def test_422_get_avis_detail(self):
    #     res = self.client().get('/avis/100')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test deleting existing avis
    # def test_delete_avis(self):
    #     res = self.client().delete('/avis/4')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
        
    # # Test 422 deleting unexisting avis
    # def test_422_delete_avis(self):
    #     res = self.client().delete('/avis/200')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test update valid avis
    # def test_update_avis(self):
    #     res = self.client().put('/avis/3', json=self.update_valid_avis)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['updated'])
        
    # # Test 422 update invalid avis
    # def test_422_update_avis(self):
    #     res = self.client().put('/avis/4', json=self.update_invalid_avis)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test 422 update unexisting avis
    # def test_422_update_avis(self):
    #     res = self.client().put('/avis/400', json=self.update_valid_avis)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    
    # # Test create a message
    # def test_create_message(self):
    #     res = self.client().post('/messages', json=self.new_valid_message)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
        
    # # Test 422 create a message
    # def test_422_create_message(self):
    #     res = self.client().post('/messages', json=self.new_invalid_message)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test retrieve all messages
    # def test_get_messages(self):
    #     res = self.client().get('/messages')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['messages'])
        
    # # Test get unique message
    # def test_get_unique_message(self):
    #     res = self.client().get('/messages/1')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['message'])
        
    # # Test 422 get unique message
    # def test_422_get_unique_message(self):
    #     res = self.client().get('/messages/100')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test deleting existing message
    # def test_delete_message(self):
    #     res = self.client().delete('/messages/5')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted'])
        
    # # Test deleting unexisting message
    # def test_422_delete_message(self):
    #     res = self.client().delete('/messages/200')
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
        
    # # Test update message
    # def test_update_message(self):
    #     res = self.client().put('/messages/1', json=self.update_valid_message)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['updated'])
        
    # # Test 422 update message
    # def test_422_update_message(self):
    #     res = self.client().put('/messages/1', json=self.update_invalid_message)
    #     data = json.loads(res.data)
        
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')
    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()