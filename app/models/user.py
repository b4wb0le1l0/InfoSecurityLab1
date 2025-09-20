from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """Модель пользователя в системе"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        """Установить пароль пользователя (хэширует пароль)"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Проверить, соответствует ли введенный пароль хэшу"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Преобразовать объект пользователя в словарь (без пароля)"""
        return {
            'id': self.id,
            'username': self.username
        }
