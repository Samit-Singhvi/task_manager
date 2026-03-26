from flask_restful import Resource
from flask import request,jsonify
import jwt
import re
from flasgger import swag_from
from helper import create_specs_from_schema_user, validateswaggerinput
from schemas import LoginSchema, SignupSchema,GeneralSchema,AdminSchema
from models import Users
from datetime import datetime
from extensions import bcrypt
from helper import AUTH_KEY
from users.helper import is_valid_password, get_signup_details, check_user_exist, insert_into_database,getcredentials,insert_token_into_db,make_admin


class Login(Resource):
    specs_dict = create_specs_from_schema_user(LoginSchema, summary="Logging in the user", tag="User", method="get")
    @swag_from(specs_dict)
    def get(self):
        data = request.args
        username, password = getcredentials(data)
        validateresult = validateswaggerinput(LoginSchema,data)
        time = datetime.now()
        time = str(time)
        if validateresult:
            return validateresult
        if not (username and password):
            raise ValueError(101)   
        current_user = Users.query.filter_by(username=username).first()
        auth_token = jwt.encode({"username": username, "password": password}, AUTH_KEY, algorithm="HS256",)
        jwt.decode(auth_token,AUTH_KEY,algorithms="HS256")
        if not current_user:
            raise ValueError(108)
        if not bcrypt.check_password_hash(current_user.password, password):
            raise ValueError(107)
        user_id = current_user.id
        insert_token_into_db(auth_token,user_id)
        return jsonify({"errorCode":0, "errorMessage": "Login successful!", "token":auth_token})
    


class Signup(Resource):
    specs_dict = create_specs_from_schema_user(SignupSchema, summary="Signing up a new user", tag="User", method="post",tokenrequired=False)
    @swag_from(specs_dict)
    def post(self):
        data = request.get_json()
        username, email, password = get_signup_details(data)
        validateerror = validateswaggerinput(SignupSchema, data)
        if validateerror:
            return validateerror
        is_valid_password(username=username, password=password)
        check_user_exist(email=email, username=username) 
        insert_into_database(email=email, username=username, password=password)
        return jsonify({"errorCode": 0, "errorMessage" : "Successfully Registered"})  
    

class MakeAdmin(Resource):
    specs_dict = create_specs_from_schema_user(AdminSchema, summary="Make a user admin", tag="Admin", method="post",tokenrequired=True)
    @swag_from(specs_dict)
    def post(self, **kwargs):
        role = kwargs.get('role')
        data = request.get_json()
        assignee_id = data.get('assignee_id')
        if role != 2:
            raise ValueError(130)
        user = Users.query.filter_by(id=assignee_id).first()
        make_admin(user)
        return jsonify({"errorCode": 0, "errorMessage" : "User successfully made admin"})


        
