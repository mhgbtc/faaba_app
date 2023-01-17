from flask import Flask, jsonify, request, abort, session
from flask_cors import CORS
from models import *
from flask_migrate import Migrate
import re
from flask_bcrypt import Bcrypt
import datetime

def create_app(test_config=None):
    # creating and configuring the app
    app = Flask(__name__)
    
    with app.app_context():
        setup_db(app)
        migrate = Migrate(app, db)
        bcrypt = Bcrypt(app)
    
    # setting up CORS
    CORS(app)
    
    # Using the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    # writing my endpoints >>>
    
    # Endpoint used to register user
    @app.route('/register', methods=['POST'])
    def register():
        body = request.get_json()
        
        firstname = body.get('firstname', None)
        lastname = body.get('lastname', None)
        email = body.get('email', None)
        password = body.get('password', None)
        confirm_password = body.get('confirm_password', None)
        phone = body.get('phone', None)
        
        #verify if there's not yet a user with the same email since it's used to be unique
        check_user = User.query.filter_by(email=email).first()
        
        if not firstname or not lastname or not email or not password or not confirm_password or not phone or not re.match(r'^\+229[0-9]{8}$', phone) or not re.match(r"[^@]+@[^@]+\.[^@]+", email) or check_user or password != confirm_password:
            abort(422)
            
        #hash the password before insertion...
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(firstname, lastname, email, password_hash, phone)
        new_user.insert()
        
        return jsonify(
            {
                "success" : True,
                "created" : new_user.id
            }
        )
    
    # Endpoint used to log user in
    @app.route('/login', methods=['POST'])
    def login():
        body = request.get_json()
        
        email = body.get("email")
        password = body.get("password")
        
        check_user = User.query.filter_by(email=email).first()
        
        if check_user and bcrypt.check_password_hash(check_user.password, password):
            return jsonify(
                {
                    "success" : True,
                    "logged" : check_user.id
                }
            )
        else:
            abort(422)
            
    # Endpoint used to retrieve all users from database
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.order_by(User.id).all()
        
        if not users:
            abort(404)
            
        return jsonify(
            {
                "success" : True,
                "users" : [user.format() for user in users]
            }
        )
        
    # Endpoint used to retrieve, modify and delete a user.
    @app.route('/users/<int:user_id>', methods=['GET', 'DELETE', 'PUT'])
    def user_manipulation(user_id):
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            
            if user is None:
                abort(404)
                
            if request.method == 'GET':
                return jsonify(
                    {
                        "success" : True,
                        "user" : user.format()
                    }
                )
            elif request.method == 'DELETE':
                user.delete()
                return jsonify(
                    {
                        "success" : True,
                        "deleted" : user.id
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                if not body.get('firstname') or not body.get('lastname') or not body.get('email') or not body.get('password') or not body.get('phone') or not re.match(r'^\+229[0-9]{8}$', body.get('phone')) or not re.match(r"[^@]+@[^@]+\.[^@]+", body.get('email')):
                    abort(422)
                
                user.firstname = body.get('firstname')
                user.lastname = body.get('lastname')
                user.email = body.get('email')
                user.password = body.get('password')
                user.sexe = body.get('sexe')
                user.city = body.get('city')
                user.birthday = body.get('birthday')
                user.phone = body.get('phone')
                user.is_phone_visible = body.get('is_phone_visible')
                user.is_driver = body.get('is_driver')
                user.profile_image = body.get('profile_image')
                user.modified_at = datetime.datetime.now(timezone('Africa/Porto-Novo'))
                
                user.update()
                return jsonify(
                    {
                        "success" : True,
                        "updated" : user.id
                    }
                )
        except:
            abort(422)
                
    # Endpoint used to retrieve all available cars and create a new one
    @app.route('/cars', methods=['GET', 'POST'])
    def get_and_create_cars():
        if request.method == 'GET':
            cars = Car.query.order_by(Car.id).all()
            
            if not cars:
                abort(404)
                
            return jsonify(
                {
                    "success" : True,
                    "cars" : [car.format() for car in cars]
                }
            )
        elif request.method == 'POST':
            body = request.get_json()
            
            user_id = body.get('user_id', None)
            mark = body.get('mark', None)
            model = body.get('model', None)
            year = body.get('year', None)
            color = body.get('color', None)
            mileage = body.get('mileage', None)
            
            if not mark or not model or not year or not color or not mileage:
                abort(422)
                
            new_car = Car(user_id, mark, model, year, color, mileage)
            new_car.insert()
            
            return jsonify(
                {
                    "success" : True,
                    "created" : new_car.id
                }
            )
    
    # Endpoint used to retrieve, modify and delete a car.
    @app.route('/cars/<int:car_id>', methods=['GET', 'DELETE', 'PUT'])
    def car_manipulation(car_id):
        try:
            car = Car.query.filter(Car.id == car_id).one_or_none()
            
            if car is None:
                abort(404)
                
            if request.method == 'GET':
                return jsonify(
                    {
                        'success' : True,
                        'car' : car.format()
                    }
                )
            elif request.method == 'DELETE':
                car.delete()
                return jsonify(
                    {
                        'success' : True,
                        'deleted' : car.id
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                if not body.get('mark') or not body.get('model') or not body.get('year') or not body.get('color') or not body.get('mileage'):
                    abort(422)
                    
                car.mark = body.get('mark')
                car.model = body.get('model')
                car.year = body.get('year')
                car.year = body.get('year')
                car.mileage = body.get('mileage')
                
                car.update()
                return jsonify(
                    {
                        'success' : True,
                        'updated' : car.id
                    }
                )
        except:
            abort(422)
    
    # Endpoint used to retrieve all trajets or create a new one
    @app.route('/trajets', methods=['GET', 'POST'])
    def get_and_create_trajets():
        if request.method == 'GET':
            trajets = Trajet.query.order_by(Trajet.id).all()
            
            if not trajets:
                abort(404)
                
            return jsonify(
                {
                    'success' : True,
                    'trajets' : [trajet.format() for trajet in trajets]
                }
            )
        elif request.method == 'POST':
            body = request.get_json()
            
            user_id = body.get('user_id', None)
            start_location = body.get('start_location', None)
            destination_location = body.get('destination_location', None)
            start_date = body.get('start_date', None)
            start_hour = body.get('start_hour', None)
            participation = body.get('participation', None)
            is_regular = body.get('is_regular', None)
            nbr_places = body.get('nbr_places', None)
            
            if not start_location or not destination_location or not start_date or not start_hour or not nbr_places:
                abort(422)
                
            new_trajet = Trajet(user_id, start_location, destination_location, start_date, start_hour, participation, is_regular, nbr_places)
            new_trajet.insert()
            
            return jsonify(
                {
                    'success' : True,
                    'created' : new_trajet.id
                }
            )
    
    # Endpoint used to manipulate trajet
    @app.route('/trajets/<int:trajet_id>', methods=['GET', 'DELETE', 'PUT'])
    def trajet_manipulation(trajet_id):
        try:
            trajet = Trajet.query.filter(Trajet.id == trajet_id).one_or_none()
            
            if trajet is None:
                abort(404)
                
            if request.method == 'GET':
                return jsonify(
                    {
                        'success' : True,
                        'trajet' : trajet.format()
                    }
                )
            elif request.method == 'DELETE':
                trajet.delete()
                return jsonify(
                    {
                        'success' : True,
                        'deleted' : trajet.id
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                if not body.get('start_location') or not body.get('destination_location') or not body.get('start_date') or not body.get('start_hour'):
                    abort(422)
                
                trajet.start_location = body.get('start_location')
                trajet.destination_location = body.get('destination_location')
                trajet.start_date = body.get('start_date')
                trajet.start_hour = body.get('start_hour')
                trajet.participation = body.get('participation')
                trajet.is_regular = body.get('is_regular')
                trajet.nbr_places = body.get('nbr_places')
                
                trajet.update()
                return jsonify(
                    {
                        'success' : True,
                        'updated' : trajet.id
                    }
                )
        except:
            abort(422)

    # Endpoint used to retrieve all reservations or create a new one
    @app.route('/reservations', methods=['GET', 'POST'])
    def get_and_create_reservations():
        if request.method == 'GET':
            reservations = Reservation.query.order_by(Reservation.id).all()
            
            if not reservations:
                abort(404)
                
            return jsonify(
                {
                    'success' : True,
                    'reservations' : [reservation.format() for reservation in reservations]
                }
            )
        elif request.method == 'POST':
            body = request.get_json()
            
            user_id = body.get('user_id')
            trajet_id = body.get('trajet_id')
            nbr_places_res = body.get('nbr_places_res')
            
            if not user_id or not trajet_id or not nbr_places_res:
                abort(422)
                
            new_reservation = Reservation(user_id, trajet_id, nbr_places_res)
            new_reservation.insert()
            
            return jsonify(
                {
                    'success' : True,
                    'created' : new_reservation.id
                }
            )
            
    # Endpoint used to manipulate reservation
    @app.route('/reservations/<int:reservation_id>', methods=['GET', 'DELETE', 'PUT'])
    def reservation_manipulation(reservation_id):
        try:
            reservation = Reservation.query.filter(Reservation.id == reservation_id).one_or_none()
            
            if reservation is None:
                abort(404)
                
            if request.method == 'GET':
                return jsonify(
                    {
                        'success' : True,
                        'reservation' : reservation.format()
                    }
                )
            elif request.method == 'DELETE':
                reservation.delete()
                return jsonify(
                    {
                        'success' : True,
                        'deleted' : reservation.id
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                if not body.get('user_id') or not body.get('trajet_id') or not body.get('nbr_places_res'):
                    abort(422)
                
                reservation.user_id = body.get('user_id')
                reservation.trajet_id = body.get('trajet_id')
                reservation.nbr_places_res = body.get('nbr_places_res')
                
                reservation.update()
                return jsonify(
                    {
                        'success' : True,
                        'updated' : reservation.id
                    }
                )
        except:
            abort(422)
    
    # Endpoint used to retrieve all avis or create a new one
    @app.route('/avis', methods=['GET', 'POST'])
    def get_and_create_avis():
        if request.method == 'GET':
            avis = Avis.query.order_by(Avis.id).all()
            
            if not avis:
                abort(404)
                
            return jsonify(
                {
                    'success' : True,
                    'avis' : [avi.format() for avi in avis]
                }
            )
        elif request.method == 'POST':
            body = request.get_json()
            
            user_id = body.get('user_id')
            receiver = body.get('receiver')
            content = body.get('content')
            
            check_receiver = User.query.filter_by(email=receiver).first()
            
            if not user_id or not receiver or not content or not check_receiver:
                abort(422)
                
            new_avis = Avis(user_id, receiver, content)
            new_avis.insert()
            
            return jsonify(
                {
                    'success' : True,
                    'created' : new_avis.id
                }
            )
    
    # Endpoint used to manipulate avis
    @app.route('/avis/<int:avis_id>', methods=['GET', 'DELETE', 'PUT'])
    def avis_manipulation(avis_id):
        try:
            avis = Avis.query.filter(Avis.id == avis_id).one_or_none()
            
            if avis is None:
                abort(404)
                
            if request.method == 'GET':
                return jsonify(
                    {
                        'success' : True,
                        'avis' : avis.format()
                    }
                )
            elif request.method == 'DELETE':
                avis.delete()
                return jsonify(
                    {
                        'success' : True,
                        'deleted' : avis.id
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                check_receiver = User.query.filter_by(email=body.get('receiver')).first()
                
                if not body.get('user_id') or not body.get('receiver') or not body.get('content') or not check_receiver:
                    abort(422)
                
                avis.user_id = body.get('user_id')
                avis.receiver = body.get('receiver')
                avis.content = body.get('content')
                
                avis.update()
                return jsonify(
                    {
                        'success' : True,
                        'updated' : avis.id
                    }
                )
        except:
            abort(422)
    
    # Endpoint used to retrieve all messages and create a new one
    @app.route('/messages', methods=['GET', 'POST'])
    def get_and_create_message():
        if request.method == 'GET':
            messages = Message.query.order_by(Message.id).all()
            
            if not messages:
                abort(404)
                
            return jsonify(
                {
                    'success' : True,
                    'messages' : [message.format() for message in messages]
                }
            )
        elif request.method == 'POST':
            body = request.get_json()
            
            user_id = body.get('user_id')
            receiver = body.get('receiver')
            content = body.get('content')
            
            check_receiver = User.query.filter_by(email=receiver).first()
            
            if not user_id or not receiver or not content or not check_receiver:
                abort(422)
                
            new_message = Message(user_id, receiver, content)
            new_message.insert()
            
            return jsonify(
                {
                    'success' : True,
                    'created' : new_message.id
                }
            )
    
    # Endpoint used to manipulate messages
    @app.route('/messages/<int:message_id>', methods=['GET', 'DELETE', 'PUT'])
    def message_manipulation(message_id):
        try:
            message = Message.query.filter(Message.id == message_id).one_or_none()
            
            if message is None:
                abort(404)
                
            if request.method == 'GET':
                return jsonify(
                    {
                        'success' : True,
                        'message' : message.format()
                    }
                )
            elif request.method == 'DELETE':
                message.delete()
                return jsonify(
                    {
                        'success' : True,
                        'deleted' : message.id
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                check_receiver = User.query.filter_by(email=body.get('receiver')).first()
                
                if not body.get('user_id') or not body.get('receiver') or not body.get('content') or not check_receiver:
                    abort(422)
                    
                message.user_id = body.get('user_id')
                message.receiver = body.get('receiver')
                message.content = body.get('content')
                message.edited_at = datetime.datetime.now(timezone('Africa/Porto-Novo'))
                
                message.update()
                return jsonify(
                    {
                        'success' : True,
                        'updated' : message.id
                    }
                )
        except:
            abort(422)
    
    # Creating error handlers for all expected errors
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request"
            }
        ), 400
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
        ), 404
        
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(
            {
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }
        ), 405
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }
        ), 422
        
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify(
            {
                "success": False,
                "error": 500,
                "message": "internal server error"
            }
        ), 500
    
    return app