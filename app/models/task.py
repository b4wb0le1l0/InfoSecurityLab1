from app.database import db

class Task(db.Model):
    """Модель задачи в системе"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Преобразовать объект задачи в словарь"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }
