from flask import Flask, request,g
from flask_restful import Api
import time, os
from dotenv import load_dotenv
from logger import logger
from error_handler import ErrorHandlingMiddleware
from flasgger import Swagger
from flask_cors import CORS
from models import db
from tasks.views import CreateTaskView, TaskView, TaskDetailView, UpdateTaskView, DeleteTaskView
from extensions import bcrypt 
from users.views import Login, Signup,MakeAdmin

load_dotenv()



SECRET_KEY = os.getenv('SECRET_KEY')
AUTH_KEY = os.getenv('AUTH_KEY')


# Creating a cursor object
app = Flask(__name__)
api = Api(app)
bcrypt.init_app(app)

app.config['PROPAGATE_EXCEPTIONS'] = True


#Important - doesn't connect to network without CORS
CORS(app)

SECRET_KEY = os.getenv('SECRET_KEY')

DEFAULT_ENDPOINT = 'apispec_1'

DEFAULT_CONFIG = {
        "title":"User and Product API",
        "termsOfService" : None,
        "description" : "This page contain several APIs for User Authentication and to access Product Database",
        "headers": [    
        ],
        "specs": [
        {
            "endpoint": DEFAULT_ENDPOINT,
            "route": f'/{DEFAULT_ENDPOINT}.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/swagger/",
        "securityDefinitions": {
    },
    }


config=DEFAULT_CONFIG
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads/')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

swagger = Swagger(app,config=config)

errorHandle = ErrorHandlingMiddleware(app)


API_ENDPOINT = '/product'

api.add_resource(Login , '/login')
api.add_resource(Signup, '/signup')
api.add_resource(CreateTaskView, '/new_task')
api.add_resource(TaskView, '/tasks')
api.add_resource(TaskDetailView, '/tasks/<int:task_id>')
api.add_resource(UpdateTaskView, '/tasks/<int:task_id>')
api.add_resource(DeleteTaskView, '/tasks/<int:task_id>')
api.add_resource(MakeAdmin, '/make_admin')


@app.before_request
def getstarttime():
    g.start = time.time()


@app.after_request
def getelapsetime(response):
    elapse_time = ""
    elapse_time = time.time() - g.start
    if response.content_type == "application/json":
        extralogdata = {
            "methodName" : request.method,
            "client_ip": request.remote_addr,
            "port": request.environ.get('SERVER_PORT'),
            "data": request.get_json(silent=True),  # 'silent=True' prevents errors if there's no JSON
            "time_taken": time.time(),
            "elapse_time": elapse_time,
        }
        
        logger.info(response.get_json().get('errorMessage'), extra=extralogdata)
    return response




if __name__ == '__main__':
    app.run(debug=True)