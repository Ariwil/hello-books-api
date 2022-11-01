import pytest
from app import create_app #going to configure create_app and db when running the tests
from app import db
from flask.signals import request_finished

@pytest.fixture #app to be used in our client fixture (explained later)
def app():
    app = create_app({"TESTING": True}) #run and create an app object (like in app/__init__.py)
    #{"TESTING": True} --> Here, we're passing in a dictionary to represent a "test config" object.
    @request_finished.connect_via(app) #this decorator indicates that the fxn below will be invoked after any request is completed
    def expire_session(sender, response, **extra):
        db.session.remove() #After a request is made in our test, this line creates a new database session so that we can test that changes were persisted in the database. This is particularly relevant for testing the update method.

    with app.app_context(): #This syntax designates that the following code should have an application context. This lets various functionality in Flask determine what the current running app is.
        db.create_all() #At the start of each test, this code recreates the tables needed for our models.
        yield app

    with app.app_context():
        db.drop_all() #drop all of the tables, deleting any data that was created during the test.

@pytest.fixture
def client(app): #request the existing app fixture to run, first.
    return app.test_client() #The responsibility of this fixture is to make a test client, which is an object able to simulate a client making HTTP requests.
