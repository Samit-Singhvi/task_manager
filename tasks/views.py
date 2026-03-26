from flask import jsonify,request
from flask_restful import Resource
from helper import create_specs_from_schema_user,create_specs_with_path_param,token_required
from flasgger import swag_from
from models import db
from models import TaskModel
from schemas import TaskSchema,TaskDeleteSchema,TaskUpdateSchema,TaskDetailViewSchema,GeneralSchema



class CreateTaskView(Resource):

    @swag_from(create_specs_from_schema_user(TaskSchema,method="POST", summary="Create a new task", tag="Tasks",tokenrequired=True))
    @token_required
    def post(self, **kwargs):
        data = request.get_json()
        user_id = kwargs.get('user_id')
        new_task = TaskModel(title=data['title'], 
        description=data.get('description', ''), user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully', 'task': {'id': new_task.id, 'title': new_task.title, 'description': new_task.description, 'completed': new_task.completed}})



class TaskView(Resource):
    @swag_from(create_specs_from_schema_user(GeneralSchema,method="GET", summary="Get all tasks for the authenticated user", tag="Tasks",tokenrequired=True,))
    @token_required
    def get(self, **kwargs):
        user_id = kwargs.get('user_id')
        print(kwargs.get('role'))
        tasks = TaskModel.query.filter_by(user_id=user_id).all()
        tasks_data = [{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks]
        return jsonify({'tasks': tasks_data})

class TaskDetailView(Resource):
    @swag_from(create_specs_with_path_param(TaskDetailViewSchema,method="GET", summary="Get a specific task by ID", tag="Tasks", tokenrequired=True,path_param_name="task_id"))
    @token_required
    def get(self, task_id, **kwargs):
        user_id = kwargs.get('user_id')
        print(kwargs.get('role'))
        task = TaskModel.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            raise ValueError(133)
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed})

class UpdateTaskView(Resource):
    @swag_from(create_specs_with_path_param(TaskUpdateSchema,method="PUT", summary="Update a specific task by ID", tag="Tasks", tokenrequired=True,path_param_name="task_id"))
    @token_required
    def put(self, task_id, **kwargs):
        user_id = kwargs.get('user_id')
        data = request.get_json()
        task = TaskModel.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        db.session.commit()
        return jsonify({'message': 'Task updated successfully', 'task': {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}})

class DeleteTaskView(Resource):
    @swag_from(create_specs_with_path_param(TaskDeleteSchema,method="DELETE", summary="Delete a specific task by ID", tag="Tasks", tokenrequired=True,path_param_name="task_id"))
    @token_required
    def delete(self, task_id, **kwargs):
        user_id = kwargs.get('user_id')
        role = kwargs.get('role')
        print(role, user_id)
        if (role!=2):
            return {"message":"Only admin can do this"}, 403
        task = TaskModel.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return {'message': 'Task not found'}, 404
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Task deleted successfully'}, 200