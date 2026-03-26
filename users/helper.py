import re
from extensions import bcrypt
from models import Users,db,Tokens
from datetime import datetime, timedelta


def is_valid_password(password="", username=""):
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!_#%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not(username and password):
        raise ValueError(101)
    if not re.match(password_regex, password):
        raise ValueError(109)

def check_user_exist(email, username):
    user_exists = Users.query.filter_by(username=username).first()
    if user_exists:
        raise ValueError(105)
    email_exist = Users.query.filter_by(email=email).first()
    if email_exist:
        raise ValueError(106)

def get_signup_details(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    return username, email, password

def insert_into_database(username, password, email):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = Users(username=username,email=email,password=hashed_password,role_id=1)
    db.session.add(new_user)
    db.session.commit()
    
def make_admin(user):
    user.role_id = 2
    db.session.commit()
    
def getcredentials(data):
    username = data.get('username')
    password = data.get('password')
    return username, password

def insert_token_into_db(token,user_id):
    created_at = datetime.now()
    expired_at = created_at + timedelta(hours=2)
    token_in_db = Tokens.query.filter_by(user_id=user_id).first()
    if not token_in_db:
        token = Tokens(
            token = token,
            user_id = user_id,
            created_at = created_at,
            expired_at = expired_at
        )
        db.session.add(token)
    else:    
        token_in_db.token = token
        token_in_db.created_at = created_at
        token_in_db.expired_at = expired_at
    db.session.commit()

def is_valid_password_username_secretkey(oldpassword="", newpassword=""):
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    
    if not(oldpassword and newpassword):
        raise ValueError(101)
    if not re.match(password_regex, newpassword):
        raise ValueError(109)

def get_password_from_user(data):
    oldpassword = data.get('oldpassword')
    newpassword = data.get('newpassword')
    return oldpassword,newpassword