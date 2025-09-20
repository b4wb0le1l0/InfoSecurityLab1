from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from app.database import db, init_db
from app.api.auth import auth_bp
from app.api.data import data_bp

def create_app():
    """Создание и настройка Flask-приложения"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_db(app)
    
    jwt = JWTManager(app)
    
    CORS(app)
    
    # Регистрация blueprint'ов
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(data_bp, url_prefix='/api/data')
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
