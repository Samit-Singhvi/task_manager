from marshmallow import ValidationError 
from flask import jsonify,request
from dotenv import load_dotenv
import os
from functools import wraps
from models import Tokens,Users
from datetime import datetime
import re

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
AUTH_KEY = os.getenv('AUTH_KEY')

def remove_last_integer_from_url(url):
    updated_url = re.sub(r'/\d+$', '/', url)
    return updated_url

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" not in request.headers:
            raise ValueError(121)
        token = request.headers.get('Authorization').split(" ")[1]
        token_in_db = Tokens.query.filter_by(token = token).first()
        if not token_in_db:
            raise ValueError(123)
        expired_at = token_in_db.expired_at
        if datetime.now()>expired_at:
            raise ValueError(120)
        user_id = token_in_db.user_id
        user = Users.query.filter_by(id=user_id).first()
        role_id = user.role_id
        return f(*args, user_id=user_id,role=role_id, **kwargs)

    return decorated



def create_specs_from_schema_user(schema,summary,tag,method,tokenrequired=False):
    parameters = {}
    auth_parameter = {
                'name': "Authorization",
                'in': 'header',
                'required': True,
                'schema' : {
                    'type': 'string',
                    'example' : 'Bearer XXXX'
                }
            }
    
    for field_name, field in schema().fields.items():
        field_type = type(field).__name__.replace('Field', '').lower()
        parameters[field_name] = {'type': field_type}

    if method.upper() == 'POST':

        query_parameters = []
        body_schema = {
            'type': 'object',
            'properties': {}
        }

        for field_name, field_info in parameters.items():
            body_schema['properties'][field_name] = {'type': field_info['type']}

        query_parameters.append({
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': body_schema
        })
        if tokenrequired:
            query_parameters.append(auth_parameter)

    elif method.upper()=="PUT":
        query_parameters = []
        body_schema = {
            'type': 'object',
            'properties': {}
        }
        for field_name, field_info in parameters.items():
            body_schema['properties'][field_name] = {'type': field_info['type']}
        
        query_parameters.append({
            'name': 'body',
            'in': 'body',
            'required': False,
            'schema': body_schema
        })
        if tokenrequired:
            query_parameters.append(auth_parameter)
    else:
        query_parameters = []
        for field_name, field_info in parameters.items():
            query_parameters.append({
                'name': field_name,
                'in': 'query',
                'required': False,
                'type': field_info['type'],
            }),
        if tokenrequired:
            query_parameters.append(auth_parameter)
    specs_dict = {
        'summary': summary,
        'parameters': query_parameters,
        'tags': [tag],
        'responses': {
            '200': {
                'description': 'Request Successful'
            }
        },
        'route': 'apidocs',
    }
    

    return specs_dict


def validateswaggerinput(schema_class,data):
        try:
            schema = schema_class()
            schema.load(data)
        except ValidationError as err:
            return jsonify({"errorCode": 400, "errorMessage": err.messages})


def create_specs_with_path_param(schema, summary, tag, method, path_param_name="id", path_param_type="integer", tokenrequired=True):
    """Create specs with path parameter support - removes id field from query and adds as path param"""
    specs = create_specs_from_schema_user(schema, summary, tag, method, tokenrequired)
    
    # Remove the path parameter field from query parameters (by name)
    # This removes both 'id' and 'task_id' etc.
    specs['parameters'] = [
        p for p in specs['parameters'] 
        if p.get('name') not in ['id', path_param_name]
    ]
    
    # Add path parameter at the beginning
    specs['parameters'].insert(0, {
        'name': path_param_name,
        'in': 'path',
        'required': True,
        'type': path_param_type
    })
    
    return specs

