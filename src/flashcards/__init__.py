from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from flask_marshmallow import Marshmallow


app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)

# create database and models
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flashcards.db"
db = SQLAlchemy(app)


from flashcards import routes
