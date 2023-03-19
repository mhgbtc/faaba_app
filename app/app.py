from flask import Flask, jsonify, request, abort, session, url_for
from flask_cors import CORS, cross_origin
from models import *
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from functools import wraps
import re
import jwt
import os


def create_app(test_config=None):
    # creating and configuring the app
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv(
        'JWT_SECRET_KEY', '53cce8ef0f5ec52663e20d19e81e5d75')
    app.config['SECRET_KEY'] = os.getenv(
        'SECRET_KEY', '8f356b6dece94176854bf3ac5dd14273')
    ALGORITHM = 'HS256'
    app.config.from_object('config')

    with app.app_context():
        setup_db(app)
        migrate = Migrate(app, db)
        bcrypt = Bcrypt(app)
        mail = Mail(app)
        mail.init_app(app)
        login_manager = LoginManager()
        login_manager.init_app(app)

    # setting up CORS
    CORS(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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

    # Generate confirmation token
    def generate_confirmation_token(email):
        payload = {
            'exp': datetime.now(timezone('Africa/Porto-Novo')) + timedelta(minutes=5),
            'iat': datetime.now(timezone('Africa/Porto-Novo')),
            'sub': email
        }
        token = jwt.encode(
            payload,
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return token

    def jwt_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')

            if not auth_header:
                return jsonify({'success': False, 'message': 'Authorization header is missing'}), 401

            try:
                token = auth_header.split(' ')[1]
                decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=[ALGORITHM])
            except jwt.ExpiredSignatureError:
                return jsonify({'success': False, 'message': 'Access token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'success': False, 'message': 'Invalid access token'}), 401

            return f(*args, **kwargs)

        return decorated_function
    
    # writing my endpoints >>>

    @app.route('/')
    def hello_world():
        return jsonify(
            {
                "message": "Salut le monde! Tout va bien GUIDJOOOO"
            }
        )

    # Endpoint used to register user
    @app.route('/register', methods=['POST'])
    def register():
        body = request.get_json()

        fullname = body.get('fullname', None)
        email = body.get('email', None)
        is_driver = body.get('is_driver', None)
        password = body.get('password', None)
        confirm_password = body.get('confirm_password', None)

        # verify if there's not yet a user with the same email since it's used to be unique
        check_user = User.query.filter_by(email=email).first()

        if not fullname or not email or not password or not confirm_password or not re.match(r"[^@]+@[^@]+\.[^@]+", email) or check_user or password != confirm_password:
            abort(422)

        # hash the password before insertion...
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(fullname, email, password_hash, is_driver)
        new_user.insert()

        # Générer un jeton JWT pour l'adresse e-mail de l'utilisateur
        token = generate_confirmation_token(new_user.email)

        # Construire le lien de confirmation
        confirmation_url = url_for(
            'confirm_email',
            token=token,
            _external=True
        )

        # Envoyer un e-mail de confirmation à l'utilisateur
        msg = Message(
            subject='Confirmation de votre adresse e-mail',
            recipients=[email],
            body=f'Cliquez sur le lien suivant pour confirmer votre adresse e-mail: {confirmation_url}'
        )
        mail.send(msg)

        return jsonify(
            {
                "success": True,
                "user_created": new_user.id,
                "message": "Confirmation email sent"
            }
        )

    @app.route('/confirm_email')
    def confirm_email():
        token = request.args.get('token')

        try:
            payload = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            email = payload['sub']

            user = User.query.filter_by(email=email).first()

            user.is_email_verified = True
            user.update()

            return jsonify(
                {
                    "message": "Votre adresse e-mail a été vérifiée avec succès!"
                }
            )

        except:
            return jsonify(
                {
                    "message": "Le lien de confirmation est invalide ou a expiré!"
                }
            )

    # Endpoint used to log user in
    @app.route('/login', methods=['POST'])
    def login():
        body = request.get_json()

        email = body.get("email")
        password = body.get("password")

        check_user = User.query.filter_by(email=email).first()

        if check_user.is_email_verified == False:
            return jsonify(
                {
                    "success": False,
                    "message": "Vous devez confirmer votre email"
                }
            ), 422

        if check_user and bcrypt.check_password_hash(check_user.password, password):
            login_user(check_user)
            session['logged_in'] = True

            # Générez un jeton d'accès
            access_token = jwt.encode(
                {
                    'user_id': check_user.id,
                    'exp': datetime.utcnow() + timedelta(minutes=30)  # Expiration du jeton en 30 minutes (modifiable)
                },
                app.config['JWT_SECRET_KEY'],
                algorithm=ALGORITHM
            )

            return jsonify(
                {
                    "success": True,
                    "user_id": check_user.id,
                    "access_token": access_token  # Retournez le jeton d'accès dans la réponse
                }
            )
        else:
            return jsonify(
                {
                    'success': False,
                    'message': "Quelque chose s'est mal passé"
                }
            ), 422

    # Logout user
    @app.route('/logout', methods=['POST'])
    @login_required
    def logout():
        session.pop('logged_in', None)
        logout_user()
        return jsonify(
            {
                'success': True,
                'message': 'Vous êtes déconnecté'
            }
        )

    # Endpoint used to retrieve all rides
    @app.route('/rides', methods=['GET'])
    def get_rides():
        query = Ride.query
            
        departure = request.args.get('departure', None)
        arrival = request.args.get('arrival', None)
        departure_date = request.args.get('departure_date', None)
        estimated_arrival_date = request.args.get('estimated_arrival_date', None)
        seats = request.args.get('seats', None)
            
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
            return jsonify(
                {
                    'success': False,
                    'message': "Aucun trajet disponible"
                }
            ),404
                
        return jsonify(
            {
                'success' : True,
                'rides' : [ride.format() for ride in rides]
            }
        )

    # Endpoint used to create new ride
    @app.route('/rides', methods=['POST'])
    @jwt_required
    def create_rides():
        if current_user.is_driver == True:
            body = request.get_json()

            driver_id = current_user.id
            departure = body.get('departure', None)
            arrival = body.get('arrival', None)
            boardingLocation = body.get('boardingLocation', None)
            departure_date = body.get('departure_date', None)
            estimated_arrival_date = body.get('estimated_arrival_date', None)
            seats = body.get('seats', None)
            price = body.get('price', None)

            if not departure or not arrival or not boardingLocation or not seats or seats < 1:
                abort(422)

            new_ride = Ride(driver_id, departure, arrival, boardingLocation,
                            departure_date, estimated_arrival_date, seats, price)
            new_ride.insert()

            return jsonify(
                {
                    'success': True,
                    'ride_created': new_ride.id
                }
            )
        else:
            return jsonify(
                {
                    "success": False,
                    "message" : "Vous devez etre conducteur pour publier"
                }
            ),403

    # Endpoint used to manipulate ride
    @app.route('/rides/<int:ride_id>', methods=['GET', 'DELETE', 'PUT'])
    @jwt_required
    def ride_manipulation(ride_id):
        try:
            ride = Ride.query.filter(Ride.id == ride_id).one_or_none()

            if ride is None:
                return jsonify(
                    {
                        'success' : False,
                        'message' : "Ce trajet n'existe pas."
                    }
                ),404

            if request.method == 'GET':
                return jsonify(
                    {
                        'success': True,
                        'ride': ride.format()
                    }
                )
            elif request.method == 'DELETE':
                ride.delete()
                return jsonify(
                    {
                        'success' : True,
                        'ride_deleted' : ride.id,
                        "message" : "Trajet supprimé"
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()

                if not body.get('departure') or not body.get('arrival') or not body.get('boardingLocation', None) or not body.get('seats') or body.get('seats') < 1:
                    abort(422)
                
                ride.driver_id = current_user.id
                ride.departure = body.get('departure', None)
                ride.boardingLocation = body.get('boardingLocation', None)
                ride.arrival = body.get('arrival', None)
                ride.departure_date = body.get('departure_date', None)
                ride.estimated_arrival_date = body.get('estimated_arrival_date', None)
                ride.seats = body.get('seats', None)
                ride.price = body.get('price', None)
                
                ride.update()
                return jsonify(
                    {
                        'success' : True,
                        'ride_updated' : ride.id,
                        "message" : "Trajet mis a jour"
                    }
                )
        except:
            return jsonify(
                {
                    'success' : False,
                    'message' : "Quelque chose s'est mal passé"
                }
            ),422

    # Endpoint used to retrieve all bookings or create a new one
    @app.route('/bookings', methods=['GET', 'POST'])
    @jwt_required
    def get_and_create_bookings():
        if request.method == 'GET':
            bookings = Booking.query.order_by(Booking.id).all()

            if not bookings:
                return jsonify(
                    {
                        'success': False,
                        'message': "Aucune reservation disponible"
                    }
                ),404

            return jsonify(
                {
                    'success': True,
                    'bookings': [booking.format() for booking in bookings]
                }
            )
        elif request.method == 'POST':
            body = request.get_json()

            passenger_id = current_user.id
            ride_id = body.get('ride_id')
            
            if not passenger_id or not ride_id:
                return jsonify(
                    {
                        'success': False,
                        'message': "Impossible de reserver"
                    }
                ),422
                
            # Check if the number of seats is suffisant
            ride = Ride.query.get(ride_id)
            
            if ride is None or ride.seats < 1:
                return jsonify(
                    {
                        'success' : False,
                        'message' : "Places insuffisantes pour la réservation."
                    }
                ), 422

            new_booking = Booking(passenger_id, ride_id)
            new_booking.insert()

            # Update the number of seats
            ride.seats -= 1
            ride.update()

            return jsonify(
                {
                    'success': True,
                    'booking_created': new_booking.id,
                    "message" : "Reservation faite"
                }
            )

    # Endpoint used to manipulate booking
    @app.route('/bookings/<int:booking_id>', methods=['GET', 'DELETE', 'PUT'])
    @jwt_required
    def booking_manipulation(booking_id):
        try:
            booking = Booking.query.filter(
                Booking.id == booking_id).one_or_none()

            if booking is None:
                return jsonify(
                    {
                        'success' : False,
                        'message' : "Reservation introuvable"
                    }
                ),404

            if request.method == 'GET':
                return jsonify(
                    {
                        'success': True,
                        'booking': booking.format()
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
                        'booking_deleted' : booking.id,
                        "message" : "Reservation supprimee"
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                passenger_id = current_user.id
                ride_id = body.get('ride_id')
                
                # Check if the number of seats is suffisant
                ride = Ride.query.get(ride_id)
                
                if ride is None:
                    return jsonify(
                        {
                            'success' : False,
                            'message' : "Mise a jour impossible : Ce trajet n'existe pas"
                        }
                    ), 422
                
                if ride.seats < 1:
                    return jsonify(
                        {
                            'success' : False,
                            'message' : "Places insuffisantes pour la réservation."
                        }
                    ), 422
                
                booking.passenger_id = passenger_id
                booking.ride_id = ride_id
                booking.update()
                
                # Update the number of seats
                ride.seats -= 1
                ride.update()
                
                return jsonify(
                    {
                        'success' : True,
                        'booking_updated' : booking.id,
                        "message" : "Mise a jour reussie"
                    }
                )
        except:
            return jsonify(
                {
                    'success' : False,
                    'message' : "Quelque chose s'est mal passé"
                }
            ),422

    # Endpoint used to retrieve all users from database
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.order_by(User.id).all()
        
        if not users:
            return jsonify(
                {
                    'success': False,
                    'message': "Aucun utilisateur inscrit"
                }
            ),404
            
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
                return jsonify(
                    {
                        "success": False,
                        "message": "Cet utilisateur n'existe pas"
                    }
                ),404
                
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
                        "user_deleted" : user.id,
                        "message": "Compte supprimé"
                    }
                )
            elif request.method == 'PUT':
                body = request.get_json()
                
                if not body.get('fullname') or not body.get('email') or not re.match(r"[^@]+@[^@]+\.[^@]+", body.get('email')):
                    return jsonify(
                        {
                            "success": False,
                            "message": "Quelque chose s'est mal passé"
                        }
                    ),422
                
                user.fullname = body.get('fullname')
                user.email = body.get('email')
                
                user.update()
                return jsonify(
                    {
                        "success" : True,
                        "user_updated" : user.id,
                        "message" : "Profile modifié"
                    }
                )
        except:
            return jsonify(
                {
                    "success": False,
                    "message": "Quelque chose s'est mal passé"
                }
            ),422

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


app = create_app()

if __name__ == '__main__':
    app.run()
