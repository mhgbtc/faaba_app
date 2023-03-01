from flask import Blueprint, jsonify, request, abort
from app import db
from models import User
from datetime import datetime
import re
import bcrypt

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/register', methods=['POST'])
def register():
        body = request.get_json()
        
        fullname = body.get('fullname', None)
        email = body.get('email', None)
        is_driver = body.get('is_driver', None)
        password = body.get('password', None)
        confirm_password = body.get('confirm_password', None)
        
        #verify if there's not yet a user with the same email since it's used to be unique
        check_user = User.query.filter_by(email=email).first()
            
        if not fullname or not is_driver or not email or not password or not confirm_password or not re.match(r"[^@]+@[^@]+\.[^@]+", email) or check_user or password != confirm_password:
            abort(422)
            
        #hash the password before insertion...
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        new_user = User(fullname, email, password_hash, is_driver)
        new_user.insert()
        
        return jsonify(
            {
                "success" : True,
                "created" : new_user.id,
                "message" : "User successfully created"
            }
        )