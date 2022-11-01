from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os #provides a way to read environment variables

db = SQLAlchemy()
migrate = Migrate()
load_dotenv() #loads the values from our .env file so that the os module is able to see them

def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")  #os.environ.get() -- This syntax gets an environment variable by the passed-in name
    else:
        app.config["TESTING"] = True #turns testing mode on
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI") #This is the exact name of the testing database environment variable we defined in .env

#these weren't in the updated learn example in 06)BaA - Testing - dotenv and the tes db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models.book import Book
    from .routes import books_bp
    app.register_blueprint(books_bp)
    
    return app