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
        self.database_name = "faabadb_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','root','localhost:5432', self.database_name)
        with self.app.app_context():
            setup_db(self.app, self.database_path)
            
        self.new_user = {
            "firstname" : "Mahougnon",
            "lastname" : "Samuel",
            "email" : "samtest18@gmail.com",
            "password" : "Test1234",
            "confirm_password" : "Test1234",
            "phone" : "+22995648125"
        }
        
        self.new_invalid_user = {
            "firstname" : "Mhg",
            "lastname" : "Ken",
            "email" : "bad",
            "password" : "test1234",
            "confirm_password" : "test1234",
            "phone" : "22995648125"
        }
        
        self.log_valid_user = {
            "email" : "samtest17@gmail.com",
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
        
        self.new_valid_trajet = {
            'user_id' : 28,
            'start_location' : "Abomey-Calavi",
            'destination_location' : "Porto-Novo",
            'start_date' : '2023-01-10',
            'start_hour' : '13:15',
            'participation' : 129,
            'is_regular' : True,
            'nbr_places' : 3    
        }
        
        self.new_invalid_trajet = {
            'destination_location' : "Porto-Novo",
            'start_date' : '2023-01-10',
            'start_hour' : '13:15',
            'participation' : 129,
            'is_regular' : True,
            'nbr_places' : 3    
        }
        
        self.update_valid_trajet = {
            'user_id' : 23,
            'start_location' : "Cotonou",
            'destination_location' : "Parakou",
            'start_date' : '2023-01-10',
            'start_hour' : '13:15',
            'participation' : 129,
            'is_regular' : True,
            'nbr_places' : 3    
        }
        
        self.update_invalid_trajet = {
            'user_id' : 28,
            'start_location' : "Cotonou",
            'start_date' : '2023-01-10',
            'start_hour' : '13:15',
            'participation' : 129,
            'is_regular' : True,
            'nbr_places' : 3    
        }
        
        self.new_valid_reservation = {
            'user_id' : 17,
            'trajet_id' : 5,
            'nbr_places_res' : 3
        }
        
        self.new_invalid_reservation = {
            'user_id' : 17,
            'nbr_places_res' : 3
        }
        
        self.update_valid_reservation = {
            'user_id' : 28,
            'trajet_id' : 8,
            'nbr_places_res' : 5
        }
        
        self.update_invalid_reservation = {
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
    
    #Testing new user insertion - Registration
    def test_create_new_user(self):
        res = self.client().post("/register", json=self.new_user)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        
    #Testing a case user provid invalid inputs
    def test_422_create_new_user(self):
        res = self.client().post("/register", json=self.new_invalid_user)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    #Testing login valid user
    def test_log_user(self):
        res = self.client().post("/login", json=self.log_valid_user)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["logged"])
        
    #Testing login invalid user
    def test_422_log_user(self):
        res = self.client().post("/login", json=self.log_invalid_user)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    #Testing retrieves users successfully
    def test_get_users(self):
        res = self.client().get("/users")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['users'])
        
    #Testing error 422 when attempting to retrieve users
    def test_422_get_users(self):
        res = self.client().get("/users/2")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    #Testing retrieve existing user detail
    def test_get_user_detail(self):
        res = self.client().get('/users/17')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])
        
    #Testing deleting an existing user
    def test_delete_user(self):
        res = self.client().delete('/users/29')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        
    #Testing deleting an unexisting user
    def test_422_delete_user(self):
        res = self.client().delete('/users/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    #Testing updating specific user who exists
    def test_update_user(self):
        res = self.client().put('/users/32', json=self.update_user)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])
        
    #Testing a case they attempt to update an unexisting user
    def test_422_update_user(self):
        res = self.client().put('/users/12', json=self.update_user)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    #Testing 422 error when update with anormal data
    def test_422_update_user(self):
        res = self.client().put('/users/33', json=self.update_invalid_user)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    #Test for successfully creating new car
    def test_create_car(self):
        res = self.client().post('/cars', json=self.new_valid_car)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        
    #Test 422 create user
    def test_422_create_car(self):
        res  = self.client().post('/cars', json=self.new_invalid_car)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    #Test for successfully retrieving all cars
    def test_get_cars(self):
        res = self.client().get('/cars')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cars'])

    #Test 422 not found cars
    def test_422_get_cars(self):
        res = self.client().get('/cars/100')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")
        
    #Test get car details
    def test_get_car_detail(self):
        res = self.client().get('/cars/10')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['car'])
        
    #Test delete car
    def test_delete_car(self):
        res = self.client().delete('/cars/5')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        
    #Test 422 delete an unexisting car
    def test_422_delete_car(self):
        res = self.client().delete('/cars/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    #Test update car
    def test_update_car(self):
        res = self.client().put('/cars/11', json=self.update_valid_car)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])
        
    #Test 422 update car : valid car but invalid user inputs
    def test_422_update_car(self):
        res = self.client().put('/cars/11', json=self.update_invalid_car)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    #Test 422 not found car to update
    def test_422_update_car(self):
        res = self.client().put('/cars/1', json=self.update_valid_car)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    #Test create new trajet
    def test_create_trajet(self):
        res = self.client().post('/trajets', json=self.new_valid_trajet)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    
    #Test 422 create new trajet
    def test_422_create_trajet(self):
        res = self.client().post('/trajets', json=self.new_invalid_trajet)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    #Test retrieve all trajets
    def test_get_trajets(self):
        res = self.client().get('/trajets')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['trajets'])
        
    #Test retrieve detail on existing unique trajet
    def test_get_trajet_detail(self):
        res = self.client().get('/trajets/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['trajet'])
        
    #Test 422 get detail on unexisting trajet
    def test_422_get_trajet_detail(self):
        res = self.client().get('/trajets/100')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    #Test delete existing trajet
    def test_delete_trajet(self):
        res = self.client().delete('/trajets/4')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        
    #Test 422 delete unexisting trajet
    def test_422_delete_trajet(self):
        res = self.client().delete('/trajets/100')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test update existing trajet
    def test_update_trajet(self):
        res = self.client().put('/trajets/7', json=self.update_valid_trajet)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])
        
    # Test 422 update unexisting trajet
    def test_422_update_trajet(self):
        res = self.client().put('/trajets/300', json=self.update_valid_trajet)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test 422 update existing trajet with invalid input
    def test_422_update_invalid_trajet(self):
        res = self.client().put('/trajets/5', json=self.new_invalid_trajet)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    # Test create new reservation
    def test_create_reservation(self):
        res = self.client().post('/reservations', json=self.new_valid_reservation)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        
    # Test 422 create new reservation
    def test_422_create_reservation(self):
        res = self.client().post('/reservations', json=self.new_invalid_reservation)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test 405 on create new reservation
    def test_405_create_reservation(self):
        res = self.client().post('/reservations/100', json=self.new_valid_reservation)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
        
    # Test to retrieve all available reservations
    def test_get_reservations(self):
        res = self.client().get('/reservations')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['reservations'])
    
    # Test get detail on single reservation
    def test_get_reservation_detail(self):
        res = self.client().get('/reservations/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['reservation'])
        
    # Test 422 retrieve infos on single unexisting reservation
    def test_422_get_reservation_detail(self):
        res = self.client().get('/reservations/100')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test delete existing reservation
    def test_delete_reservation(self):
        res = self.client().delete('/reservations/3')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        
    # Test 422 delete unexisting reservation
    def test_422_delete_reservation(self):
        res = self.client().delete('/reservations/100')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test update reservation
    def test_update_reservation(self):
        res = self.client().put('/reservations/1', json=self.update_valid_reservation)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])
        
    # Test 422 update existing reservation with invalid inputs
    def test_422_update_reservation(self):
        res = self.client().put('/reservations/1', json=self.update_invalid_reservation)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    # Test create new avis
    def test_create_avis(self):
        res = self.client().post('/avis', json=self.new_valid_avis)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        
    # Test 422 create new avis
    def test_422_create_avis(self):
        res = self.client().post('/avis', json=self.new_invalid_avis)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test retrieve all avis
    def test_get_avis(self):
        res = self.client().get('/avis')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['avis'])
        
    # Test get unique avis detail
    def test_get_avis_detail(self):
        res = self.client().get('/avis/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['avis'])
        
    # Test fail get unexisting avis detail
    def test_422_get_avis_detail(self):
        res = self.client().get('/avis/100')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test deleting existing avis
    def test_delete_avis(self):
        res = self.client().delete('/avis/4')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        
    # Test 422 deleting unexisting avis
    def test_422_delete_avis(self):
        res = self.client().delete('/avis/200')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test update valid avis
    def test_update_avis(self):
        res = self.client().put('/avis/3', json=self.update_valid_avis)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])
        
    # Test 422 update invalid avis
    def test_422_update_avis(self):
        res = self.client().put('/avis/4', json=self.update_invalid_avis)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test 422 update unexisting avis
    def test_422_update_avis(self):
        res = self.client().put('/avis/400', json=self.update_valid_avis)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    # Test create a message
    def test_create_message(self):
        res = self.client().post('/messages', json=self.new_valid_message)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        
    # Test 422 create a message
    def test_422_create_message(self):
        res = self.client().post('/messages', json=self.new_invalid_message)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test retrieve all messages
    def test_get_messages(self):
        res = self.client().get('/messages')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['messages'])
        
    # Test get unique message
    def test_get_unique_message(self):
        res = self.client().get('/messages/1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])
        
    # Test 422 get unique message
    def test_422_get_unique_message(self):
        res = self.client().get('/messages/100')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test deleting existing message
    def test_delete_message(self):
        res = self.client().delete('/messages/5')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        
    # Test deleting unexisting message
    def test_422_delete_message(self):
        res = self.client().delete('/messages/200')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    # Test update message
    def test_update_message(self):
        res = self.client().put('/messages/1', json=self.update_valid_message)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])
        
    # Test 422 update message
    def test_422_update_message(self):
        res = self.client().put('/messages/1', json=self.update_invalid_message)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()