import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import create_app
from app.models.user import User
from app.models.task import Task
from app.database import db

class BasicTestCase(unittest.TestCase):
    """Базовый тестовый класс для проверки моделей пользователя и задачи"""
    def setUp(self):
        """Настройка тестового клиента и инициализация базы данных"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lab:lab@localhost:5432/lab1'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Очистка базы данных после каждого теста"""
        with self.app.app_context():
            db.drop_all()
    
    def test_user_model(self):
        """Тест создания модели пользователя и её методов"""
        with self.app.app_context():
            user = User(username='testuser')
            user.set_password('testpass')
            
            db.session.add(user)
            db.session.commit()
            
            self.assertEqual(user.username, 'testuser')
            self.assertTrue(user.check_password('testpass'))
            self.assertFalse(user.check_password('wrongpass'))
            
            user_dict = user.to_dict()
            self.assertEqual(user_dict['username'], 'testuser')
            self.assertNotIn('password_hash', user_dict)
    
    def test_task_model(self):
        """Тест создания модели задачи и её методов"""
        with self.app.app_context():
            task = Task(title='Test Task', description='Test Description')
            
            db.session.add(task)
            db.session.commit()
            
            self.assertEqual(task.title, 'Test Task')
            self.assertEqual(task.description, 'Test Description')
            
            task_dict = task.to_dict()
            self.assertEqual(task_dict['title'], 'Test Task')
            self.assertEqual(task_dict['description'], 'Test Description')

if __name__ == '__main__':
    unittest.main()
