import pytest
from models import db, Users
from app import app 
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BaseClass
from users import signup as sp


@pytest.fixture
def test_client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    with app.test_client() as testing_client:
        yield testing_client
    with app.app_context():
        db.drop_all()


# def test_signup(client, db_session):
#     response = client.post('/signup', json={
#         'username': 'testuser', 
#         'email': 'testuser@example.com', 
#         'password': 'Test@1234', 
#         'address': '123 Street'
#     })
    
#     assert response.status_code == 200
#     data = response.get_json()
#     if response.status_code == 0:
#         assert data['errorCode'] == 0
#     else:
#         assert data['errorCode'] == 1
#         assert data['errorMessage'] == 'Username is taken, please choose a new username to register'

#     user = db_session.query(Users).filter_by(username='testuser').first()
#     assert user is not None
#     assert user.email == 'testuser@example.com'

# def test_login(client, db_session):
#     response = client.get('/login', query_string={'username': 'testuser', 'password':'Test@1234'})
#     print("Authorization : ", response.get_json().get('token'))
#     assert response.status_code == 200

@pytest.fixture(scope='function')
def mock_db():
    
    # Create an in-memory SQLite database (or another database)
    engine = create_engine('sqlite:///:memory:')  # For testing, use SQLite in-memory
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create all tables in the database for testing
    Base.metadata.create_all(engine)

    # Yield the session for the test
    yield session

    # After the test, close the session and drop all tables
    session.close()
    Base.metadata.drop_all(engine)

def test_signup_user_already_exists(test_client, mocker):
    mocker.patch('models.Users.query.filter_by', return_value=mocker.Mock(first=lambda: True))
    data = {
        "username": "existing_user",
        "email": "existing@example.com",
        "password": "password123",
        "address": "123 Test St"
    }
    response = test_client.post('/signup', json=data)
    assert response.status_code == 400
    assert response.json == {"errorCode": 105, "errorMessage": "User already exists"}


def test_insert_user(mock_db, mocker):
    mock_add = mocker.patch('models.db.session.add')
    mock_commit = mocker.patch('models.db.session.commit')

    sp.insert_into_database(username="test_user", password="password123", email="test@example.com", address="456 Test St")

    mock_add.assert_called_once()
    mock_commit.assert_called_once()

def test_signup_successful(test_client, mocker):
    mocker.patch('models.Users.query.filter_by', return_value=mocker.Mock(first=lambda: None))
    mocker.patch('models.db.session.add')
    mocker.patch('models.db.session.commit')
    data = {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "password123",
        "address": "789 Test Blvd"
    }
    response = test_client.post('/signup', json=data)
    assert response.status_code == 200
    assert response.json == {"errorCode": 0, "errorMessage": "Successfully Registered"}



