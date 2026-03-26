# run this as a one-time script, e.g. reset_db.py

from models import db  # replace with your actual imports
from app import app  # replace with your actual app instance

with app.app_context():
    db.drop_all()    # drops all existing tables
    db.create_all()  # recreates tables from current models
    print("Database reset successfully.")