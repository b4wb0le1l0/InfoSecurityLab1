from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskSchema
from app.database import db
import bleach

data_bp = Blueprint('data', __name__)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@data_bp.before_request
@jwt_required()
def before_request():
    """Проверка аутентификации для всех endpoints данных"""
    pass

@data_bp.route('/', methods=['GET'])
def get_all_tasks():
    """Получить все задачи"""
    tasks = Task.query.all()
    return jsonify(tasks_schema.dump(tasks)), 200

@data_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Получить конкретную задачу по ID"""
    task = Task.query.get_or_404(task_id)
    return jsonify(task_schema.dump(task)), 200

@data_bp.route('/', methods=['POST'])
def create_task():
    """Создать новую задачу"""
    try:
        # Валидируем данные запроса
        data = task_schema.load(request.get_json())
    except Exception as e:
        return jsonify({'message': 'Invalid input data', 'error': str(e)}), 400
    
    # Очищаем входные данные для предотвращения XSS
    title = bleach.clean(data['title'])
    description = bleach.clean(data['description']) if data['description'] else None
    
    # Создаем новую задачу
    task = Task(title=title, description=description)
    
    # Сохраняем задачу в базе данных
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task_schema.dump(task)), 201

@data_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Обновить существующую задачу"""
    task = Task.query.get_or_404(task_id)
    
    try:
        # Валидируем данные запроса
        data = task_schema.load(request.get_json())
    except Exception as e:
        return jsonify({'message': 'Invalid input data', 'error': str(e)}), 400
    
    # Очищаем входные данные для предотвращения XSS
    task.title = bleach.clean(data['title'])
    task.description = bleach.clean(data['description']) if data['description'] else None
    
    # Сохраняем изменения в базе данных
    db.session.commit()
    
    return jsonify(task_schema.dump(task)), 200

@data_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удалить задачу"""
    task = Task.query.get_or_404(task_id)
    
    # Удаляем задачу из базы данных
    db.session.delete(task)
    db.session.commit()
    
    return '', 204
