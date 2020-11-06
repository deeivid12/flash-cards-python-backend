#from models import models
from flask import Flask, request, jsonify
from flask_api import status
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json
from datetime import datetime
import copy

all_decks_db = list()

app = Flask(__name__)
CORS(app)

# create database and models

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flashcards.db"
db = SQLAlchemy(app)


class Deck(db.Model):
    # __tablename__ = "decks"
    id_deck = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    #creation_date = db.Column(db.DateTime, nullable=False,
    #                          default=datetime.utcnow)
    #update_date = db.Column(db.DateTime, nullable=False,
    #                        default=copy.deepcopy(creation_date))
    recently_created = True
    cards = db.relationship("Card", backref="cards")
    # reviews_today = 0
    # reviews_per_day = 0
    # total_reviews = 0


class Card(db.Model):
    # __tablename__ = "cards"
    id_card = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)
    #creation_date = db.Column(db.DateTime, nullable=False,
    #                          default=datetime.utcnow)
    #update_date = db.Column(db.DateTime, nullable=False,
    #                        default=copy.deepcopy(creation_date))
    grade = db.Column(db.Integer, nullable=False, default=0)
    #last_review = db.Column(db.DateTime, nullable=False, default=None)
    recently_created = True
    id_deck = db.Column(db.Integer, db.ForeignKey("deck.id_deck"), nullable=False)
    # num_reviews = 0
    # box = 1


@app.route("/create_deck", methods=["POST"])
def create_deck():
    name = request.json["name"]
    description = request.json["description"]
    new_deck = Deck(name=name, description=description)
    db.session.add(new_deck)
    db.session.commit()
    return {"response": "ok!"}, status.HTTP_200_OK


@app.route("/create_card", methods=["POST"])
def create_card():
    front = request.json["front"]
    back = request.json["back"]
    id_deck = request.json["id_deck"]
    new_card = Card(back=back, front=front, id_deck=id_deck)
    db.session.add(new_card)
    db.session.commit()
    return {"response": "ok!"}, status.HTTP_200_OK


""" The following routes have not been refactored yet, so currently they are not using
SQLAlchemy ORM.

@app.route("/my_decks")    
def get_all_decks():
    results = [deck.to_dict() for deck in all_decks_db]
    return json.dumps({"results": results}), status.HTTP_200_OK


@app.route("/edit_deck", methods=["PUT"])
def edit_deck():
    id_deck = request.json["id_deck"]
    name = request.json["name"]
    description = request.json["description"]
    for i, deck in enumerate(all_decks_db):
        if id_deck == deck.id_deck:
            all_decks_db[i].name = name
            all_decks_db[i].description = description
            all_decks_db[i].update_date_now()
            return json.dumps({"results":"ok!"}), status.HTTP_200_OK
    return json.dumps({"results":"id_deck not found!"}), status.HTTP_404_NOT_FOUND


@app.route("/delete_deck", methods=["DELETE"])
def delete_deck():
    id_deck = request.json["id_deck"]
    for deck in all_decks_db:
        if id_deck == deck.id_deck:
            all_decks_db.remove(deck)
            return json.dumps({"results":"ok!"}), status.HTTP_200_OK
    return json.dumps({"results":"id_deck not found!"}), status.HTTP_404_NOT_FOUND


@app.route("/my_cards", methods=["POST"])    
def get_all_cards_from_deck():
    id_deck = request.json["id_deck"]
    for deck in all_decks_db:
        if id_deck == deck.id_deck:
            results = [card.to_dict() for card in deck.cards]
            return json.dumps({"results": results}), status.HTTP_200_OK
    return {"response":"id_deck not found!"}, status.HTTP_404_NOT_FOUND


@app.route("/review_cards", methods=["POST"])
def review_cards():
    num_cards_review = 5 # note: i have to put this configuration in a config.ini
    id_deck = request.json["id_deck"]
    all_cards = []
    for deck in all_decks_db:
        if id_deck == deck.id_deck:
            all_cards = [card.to_dict() for card in deck.cards]
            return json.dumps({"results": sorted(all_cards, key=lambda x: x["grade"])[:num_cards_review]}), status.HTTP_200_OK
    return {"response":"id_deck not found!"}, status.HTTP_404_NOT_FOUND


@app.route("/evaluate_card", methods=["PUT"])
def evaluate_card():
    id_deck = request.json["id_deck"]
    id_card = request.json["id_card"]
    grade = request.json["grade"]
    for deck in all_decks_db:
        if id_deck == deck.id_deck:
            for card in deck.cards:
                if id_card == card.id_card:
                    card.update_grade(grade)
                    card.update_last_review()
                    return json.dumps({"results":"ok!"}), status.HTTP_200_OK


def store_data():
    deck = Deck(name="deck1111", description="este es un deck de prueba")
    db.session.add(deck)
    db.session.commit()
    
"""

if __name__ == "__main__":
    app.run(debug=True)
    # store_data()