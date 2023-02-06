from flask import Flask, jsonify, request, abort, session
from flask_cors import CORS
from models import *
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from functools import wraps
import re
import jwt

def create_app(test_config=None):
    # creating and configuring the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '8f356b6dece94176854bf3ac5dd14273'
    
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
    
    def token_required(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return jsonify({'Alert!': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
            except:
                return jsonify({'Message': 'Invalid token'}), 403
            
            return func(*args, **kwargs)
        return decorated
    
    # writing my endpoints >>>
    
    # Endpoint used to register user
    @app.route('/register', methods=['POST'])
    def register():
        body = request.get_json()
        
        email = body.get('email', None)
        password = body.get('password', None)
        confirm_password = body.get('confirm_password', None)
        # firstname = body.get('firstname', None)
        # lastname = body.get('lastname', None)
        # phone = body.get('phone', None)
        
        #verify if there's not yet a user with the same email since it's used to be unique
        check_user = User.query.filter_by(email=email).first()
        
        # if not firstname or not lastname or not email or not password or not confirm_password or not phone or not re.match(r'^\+229[0-9]{8}$', phone) or not re.match(r"[^@]+@[^@]+\.[^@]+", email) or check_user or password != confirm_password:
        #     abort(422)
            
        if not email or not password or not confirm_password or not re.match(r"[^@]+@[^@]+\.[^@]+", email) or check_user or password != confirm_password:
            abort(422)
            
        #hash the password before insertion...
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(email, password_hash)
        new_user.insert()
        
        # login_user(user)
        session['logged_in'] = True
        
        token = jwt.encode(
            {
                'user': new_user.id,
                'expiration': str(datetime.utcnow() + timedelta(seconds=120))
            },
            app.config['SECRET_KEY']
        )
        
        return jsonify(
            {
                "success" : True,
                "created" : new_user.id,
                'token': token.encode('utf-8').decode('utf-8')
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
            
            # login_user(user)
            session['logged_in'] = True
            
            token = jwt.encode(
                {
                    'user': check_user.id,
                    'expiration': str(datetime.utcnow() + timedelta(seconds=120))
                },
                app.config['SECRET_KEY']
            )
            
            return jsonify(
                {
                    "success" : True,
                    "logged" : check_user.id,
                    'token': token.encode('utf-8').decode('utf-8')
                }
            )
        else:
            abort(422)
            
    # Logout user
    @app.route("/logout", methods=["POST"])
    def logout():
        # déconnecter l'utilisateur

        # renvoyer le message de succès
        return jsonify(message="L'utilisateur a été déconnecté avec succès."), 200
    
    # # Endpoint used to retrieve all users from database
    # @app.route('/users', methods=['GET'])
    # def get_users():
    #     users = User.query.order_by(User.id).all()
        
    #     if not users:
    #         abort(404)
            
    #     return jsonify(
    #         {
    #             "success" : True,
    #             "users" : [user.format() for user in users]
    #         }
    #     )
    
    # Endpoint used to retrieve all rides or create a new one
    @app.route('/rides', methods=['GET', 'POST'])
    def get_and_create_rides():
        if request.method == 'GET':
            body = request.get_json()
            
            departure = body.get('departure', None)
            arrival = body.get('arrival', None)
            departure_date = body.get('departure_date', None)
            estimated_arrival_date = body.get('estimated_arrival_date', None)
            seats = body.get('seats', None)
            
            query = Ride.query
            
            if departure is not None:
                query = query.filter(Ride.departure.ilike("%" + departure + "%"))
            if arrival is not None:
                query = query.filter(Ride.arrival.ilike("%" + arrival + "%"))
            if departure_date is not None:
                query = query.filter_by(departure_date=departure_date)
            if estimated_arrival_date is not None:
                query = query.filter_by(estimated_arrival_date=estimated_arrival_date)
            if seats is not None:
                query = query.filter_by(seats=seats)
            
            rides = query.all()
            
            if not rides:
                abort(404)
                
            return jsonify(
                {
                    'success' : True,
                    'rides' : [ride.format() for ride in rides]
                }
            )
        elif request.method == 'POST':
            body = request.get_json()
            
            driver_id = body.get('driver_id', None)
            departure = body.get('departure', None)
            arrival = body.get('arrival', None)
            departure_date = body.get('departure_date', None)
            estimated_arrival_date = body.get('estimated_arrival_date', None)
            seats = body.get('seats', None)
            
            if not departure or not arrival or not seats or seats < 1:
                abort(422)
                
            new_ride = Ride(driver_id, departure, arrival, departure_date, estimated_arrival_date, seats)
            new_ride.insert()
            
            return jsonify(
                {
                    'success' : True,
                    'created' : new_ride.id
                }
            )
    
    # Endpoint used to manipulate ride
    @app.route('/rides/<int:ride_id>', methods=['GET', 'DELETE', 'PUT'])
    @token_required
    def ride_manipulation(ride_id):
        try:
            ride = Ride.query.filter(Ride.id == ride_id).one_or_none()
            
            if ride is None:
                abort(404)
                
            if request.method == 'GET':
                return jsonify(
                    {
                        'success' : True,
                        'ride' : ride.format()
                    }
                )
            elif request.method == 'DELETE':
                ride.delete()
                return jsonify(
                    {
                        'success' : True,
                        'deleted' : ride.id
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                if not body.get('driver_id') or not body.get('departure') or not body.get('arrival') or not body.get('seats') or body.get('seats') < 1:
                    abort(422)
                
                ride.driver_id = body.get('driver_id', None)
                ride.departure = body.get('departure', None)
                ride.arrival = body.get('arrival', None)
                ride.departure_date = body.get('departure_date', None)
                ride.estimated_arrival_date = body.get('estimated_arrival_date', None)
                ride.seats = body.get('seats', None)
                
                ride.update()
                return jsonify(
                    {
                        'success' : True,
                        'updated' : ride.id
                    }
                )
        except:
            abort(422)

    # Endpoint used to retrieve all bookings or create a new one
    @app.route('/bookings', methods=['GET', 'POST'])
    def get_and_create_bookings():
        if request.method == 'GET':
            bookings = Booking.query.order_by(Booking.id).all()
            
            if not bookings:
                abort(404)
                
            return jsonify(
                {
                    'success' : True,
                    'bookings' : [booking.format() for booking in bookings]
                }
            )
        elif request.method == 'POST':
            body = request.get_json()
            
            passenger_id = body.get('passenger_id')
            ride_id = body.get('ride_id')
            
            if not passenger_id or not ride_id:
                abort(422)
                
            # Check if the number of seats is suffisant
            ride = Ride.query.get(ride_id)
            
            if ride is None or ride.seats < 1:
                return jsonify(
                    {
                        'success' : False,
                        'message' : "Places insuffisantes pour la réservation."
                    }
                ), 400

                
            new_booking = Booking(passenger_id, ride_id)
            new_booking.insert()
            
            # Update the number of seats
            ride.seats -= 1
            ride.update()
            
            return jsonify(
                {
                    'success' : True,
                    'created' : new_booking.id
                }
            )
            
    # Endpoint used to manipulate booking
    @app.route('/bookings/<int:booking_id>', methods=['GET', 'DELETE', 'PUT'])
    def booking_manipulation(booking_id):
        try:
            booking = Booking.query.filter(Booking.id == booking_id).one_or_none()
            
            if booking is None:
                abort(404)
                
            if request.method == 'GET':
                return jsonify(
                    {
                        'success' : True,
                        'booking' : booking.format()
                    }
                )
            elif request.method == 'DELETE':
                ride = Ride.query.get(booking.ride_id)
                
                # Supprimer la reservation
                booking.delete()
                
                # restaurer le nombre de seats
                ride.seats += 1
                
                # Mettre a jour rides
                ride.update()

                return jsonify(
                    {
                        'success' : True,
                        'deleted' : booking.id
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                passenger_id = body.get('passenger_id')
                ride_id = body.get('ride_id')
                
                # Check if the number of seats is suffisant
                ride = Ride.query.get(ride_id)
                
                if ride is None or ride.seats < 1:
                    return jsonify(
                        {
                            'success' : False,
                            'message' : "Places insuffisantes pour la réservation."
                        }
                    ), 400
                    
                if not passenger_id or not ride_id:
                    abort(422)
                
                booking.passenger_id = passenger_id
                booking.ride_id = ride_id
                booking.update()
                
                # Update the number of seats
                ride.seats -= 1
                ride.update()
                
                return jsonify(
                    {
                        'success' : True,
                        'updated' : booking.id
                    }
                )
        except:
            abort(422)
        
    # # Endpoint used to retrieve, modify and delete a user.
    # @app.route('/users/<int:user_id>', methods=['GET', 'DELETE', 'PUT'])
    # def user_manipulation(user_id):
    #     try:
    #         user = User.query.filter(User.id == user_id).one_or_none()
            
    #         if user is None:
    #             abort(404)
                
    #         if request.method == 'GET':
    #             return jsonify(
    #                 {
    #                     "success" : True,
    #                     "user" : user.format()
    #                 }
    #             )
    #         elif request.method == 'DELETE':
    #             user.delete()
    #             return jsonify(
    #                 {
    #                     "success" : True,
    #                     "deleted" : user.id
    #                 }
    #             )
    #         elif request.method == 'PUT':
    #             body = request.get_json()
                
    #             if not body.get('firstname') or not body.get('lastname') or not body.get('email') or not body.get('password') or not body.get('phone') or not re.match(r'^\+229[0-9]{8}$', body.get('phone')) or not re.match(r"[^@]+@[^@]+\.[^@]+", body.get('email')):
    #                 abort(422)
                
    #             user.firstname = body.get('firstname')
    #             user.lastname = body.get('lastname')
    #             user.email = body.get('email')
    #             user.password = body.get('password')
    #             user.sexe = body.get('sexe')
    #             user.city = body.get('city')
    #             user.birthday = body.get('birthday')
    #             user.phone = body.get('phone')
    #             user.is_phone_visible = body.get('is_phone_visible')
    #             user.is_driver = body.get('is_driver')
    #             user.profile_image = body.get('profile_image')
    #             user.modified_at = datetime.datetime.now(timezone('Africa/Porto-Novo'))
                
    #             user.update()
    #             return jsonify(
    #                 {
    #                     "success" : True,
    #                     "updated" : user.id
    #                 }
    #             )
    #     except:
    #         abort(422)
                
    # # Endpoint used to retrieve all available cars and create a new one
    # @app.route('/cars', methods=['GET', 'POST'])
    # def get_and_create_cars():
    #     if request.method == 'GET':
    #         cars = Car.query.order_by(Car.id).all()
            
    #         if not cars:
    #             abort(404)
                
    #         return jsonify(
    #             {
    #                 "success" : True,
    #                 "cars" : [car.format() for car in cars]
    #             }
    #         )
    #     elif request.method == 'POST':
    #         body = request.get_json()
            
    #         user_id = body.get('user_id', None)
    #         mark = body.get('mark', None)
    #         model = body.get('model', None)
    #         year = body.get('year', None)
    #         color = body.get('color', None)
    #         mileage = body.get('mileage', None)
            
    #         if not mark or not model or not year or not color or not mileage:
    #             abort(422)
                
    #         new_car = Car(user_id, mark, model, year, color, mileage)
    #         new_car.insert()
            
    #         return jsonify(
    #             {
    #                 "success" : True,
    #                 "created" : new_car.id
    #             }
    #         )
    
    # # Endpoint used to retrieve, modify and delete a car.
    # @app.route('/cars/<int:car_id>', methods=['GET', 'DELETE', 'PUT'])
    # def car_manipulation(car_id):
    #     try:
    #         car = Car.query.filter(Car.id == car_id).one_or_none()
            
    #         if car is None:
    #             abort(404)
                
    #         if request.method == 'GET':
    #             return jsonify(
    #                 {
    #                     'success' : True,
    #                     'car' : car.format()
    #                 }
    #             )
    #         elif request.method == 'DELETE':
    #             car.delete()
    #             return jsonify(
    #                 {
    #                     'success' : True,
    #                     'deleted' : car.id
    #                 }
    #             )
    #         elif request.method == 'PUT':
    #             body = request.get_json()
                
    #             if not body.get('mark') or not body.get('model') or not body.get('year') or not body.get('color') or not body.get('mileage'):
    #                 abort(422)
                    
    #             car.mark = body.get('mark')
    #             car.model = body.get('model')
    #             car.year = body.get('year')
    #             car.year = body.get('year')
    #             car.mileage = body.get('mileage')
                
    #             car.update()
    #             return jsonify(
    #                 {
    #                     'success' : True,
    #                     'updated' : car.id
    #                 }
    #             )
    #     except:
    #         abort(422)
    
    # # Endpoint used to retrieve all avis or create a new one
    # @app.route('/avis', methods=['GET', 'POST'])
    # def get_and_create_avis():
    #     if request.method == 'GET':
    #         avis = Avis.query.order_by(Avis.id).all()
            
    #         if not avis:
    #             abort(404)
                
    #         return jsonify(
    #             {
    #                 'success' : True,
    #                 'avis' : [avi.format() for avi in avis]
    #             }
    #         )
    #     elif request.method == 'POST':
    #         body = request.get_json()
            
    #         user_id = body.get('user_id')
    #         receiver = body.get('receiver')
    #         content = body.get('content')
            
    #         check_receiver = User.query.filter_by(email=receiver).first()
            
    #         if not user_id or not receiver or not content or not check_receiver:
    #             abort(422)
                
    #         new_avis = Avis(user_id, receiver, content)
    #         new_avis.insert()
            
    #         return jsonify(
    #             {
    #                 'success' : True,
    #                 'created' : new_avis.id
    #             }
    #         )
    
    # # Endpoint used to manipulate avis
    # @app.route('/avis/<int:avis_id>', methods=['GET', 'DELETE', 'PUT'])
    # def avis_manipulation(avis_id):
    #     try:
    #         avis = Avis.query.filter(Avis.id == avis_id).one_or_none()
            
    #         if avis is None:
    #             abort(404)
                
    #         if request.method == 'GET':
    #             return jsonify(
    #                 {
    #                     'success' : True,
    #                     'avis' : avis.format()
    #                 }
    #             )
    #         elif request.method == 'DELETE':
    #             avis.delete()
    #             return jsonify(
    #                 {
    #                     'success' : True,
    #                     'deleted' : avis.id
    #                 }
    #             )
    #         elif request.method == 'PUT':
    #             body = request.get_json()
                
    #             check_receiver = User.query.filter_by(email=body.get('receiver')).first()
                
    #             if not body.get('user_id') or not body.get('receiver') or not body.get('content') or not check_receiver:
    #                 abort(422)
                
    #             avis.user_id = body.get('user_id')
    #             avis.receiver = body.get('receiver')
    #             avis.content = body.get('content')
                
    #             avis.update()
    #             return jsonify(
    #                 {
    #                     'success' : True,
    #                     'updated' : avis.id
    #                 }
    #             )
    #     except:
    #         abort(422)
    
    # # Endpoint used to retrieve all messages and create a new one
    # @app.route('/messages', methods=['GET', 'POST'])
    # def get_and_create_message():
    #     if request.method == 'GET':
    #         messages = Message.query.order_by(Message.id).all()
            
    #         if not messages:
    #             abort(404)
                
    #         return jsonify(
    #             {
    #                 'success' : True,
    #                 'messages' : [message.format() for message in messages]
    #             }
    #         )
    #     elif request.method == 'POST':
    #         body = request.get_json()
            
    #         user_id = body.get('user_id')
    #         receiver = body.get('receiver')
    #         content = body.get('content')
            
    #         check_receiver = User.query.filter_by(email=receiver).first()
            
    #         if not user_id or not receiver or not content or not check_receiver:
    #             abort(422)
                
    #         new_message = Message(user_id, receiver, content)
    #         new_message.insert()
            
    #         return jsonify(
    #             {
    #                 'success' : True,
    #                 'created' : new_message.id
    #             }
    #         )
    
    # # Endpoint used to manipulate messages
    # @app.route('/messages/<int:message_id>', methods=['GET', 'DELETE', 'PUT'])
    # def message_manipulation(message_id):
    #     try:
    #         message = Message.query.filter(Message.id == message_id).one_or_none()
            
    #         if message is None:
    #             abort(404)
                
    #         if request.method == 'GET':
    #             return jsonify(
    #                 {
    #                     'success' : True,
    #                     'message' : message.format()
    #                 }
    #             )
    #         elif request.method == 'DELETE':
    #             message.delete()
    #             return jsonify(
    #                 {
    #                     'success' : True,
    #                     'deleted' : message.id
    #                 }
    #             )
    #         elif request.method == 'PUT':
    #             body = request.get_json()
                
    #             check_receiver = User.query.filter_by(email=body.get('receiver')).first()
                
    #             if not body.get('user_id') or not body.get('receiver') or not body.get('content') or not check_receiver:
    #                 abort(422)
                    
    #             message.user_id = body.get('user_id')
    #             message.receiver = body.get('receiver')
    #             message.content = body.get('content')
    #             message.edited_at = datetime.datetime.now(timezone('Africa/Porto-Novo'))
                
    #             message.update()
    #             return jsonify(
    #                 {
    #                     'success' : True,
    #                     'updated' : message.id
    #                 }
    #             )
    #     except:
    #         abort(422)
    
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