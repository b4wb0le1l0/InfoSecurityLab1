from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.schemas.auth import SignInSchema, SignUpSchema
from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import bleach

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/sign-in', methods=['POST'])
def sign_in():
    """Аутентификация пользователя по имени и паролю"""
    schema = SignInSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        return jsonify({'message': 'Invalid input data', 'error': str(e)}), 400
    
    username = bleach.clean(data['username'])
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/sign-up', methods=['POST'])
def sign_up():
    """Регистрация нового пользователя"""
    schema = SignUpSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        return jsonify({'message': 'Invalid input data', 'error': str(e)}), 400
    
    username = bleach.clean(data['username'])
    password = data['password']
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    user = User(username=username)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 201
