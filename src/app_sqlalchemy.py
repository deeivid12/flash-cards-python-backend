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
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)

# create database and models

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flashcards.db"
db = SQLAlchemy(app)


class Deck(db.Model):
    __tablename__ = "decks"
    id_deck = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recently_created = True
    cards = db.relationship("Card", backref="cards")
    # reviews_today = 0
    # reviews_per_day = 0
    # total_reviews = 0

    def update_date_now(self):
        self.update_date = datetime.utcnow()
        if self.recently_created:
            self.recently_created = False

    def to_dict(self):
        return {"id_deck": self.id_deck, "name": self.name, "description": self.description,
              "creation_date": self.creation_date.__str__(),
              "update_date": self.update_date.__str__()}


class Card(db.Model):
    __tablename__ = "cards"
    id_card = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    grade = db.Column(db.Integer, nullable=False, default=0)
    last_review = db.Column(db.DateTime, default=None)
    recently_created = True
    id_deck = db.Column(db.Integer, db.ForeignKey("decks.id_deck"), nullable=False)
    # num_reviews = 0
    # box = 1

    def to_dict(self):
        return {"id_card": self.id_card, "front": self.front,
                "back": self.back, "id_deck": self.id_deck,
                "grade": self.grade, "update_date": self.update_date.__str__(),
                "creation_date": self.creation_date.__str__(), "last_review": self.last_review.__str__()}

    def update_grade(self, grade):
        self.grade = grade

    def update_date_now(self):
        self.update_date = datetime.utcnow()
        if self.recently_created:
            self.recently_created = False

    def update_last_review(self):
        self.last_review = datetime.utcnow()


@app.route("/create_deck", methods=["POST"])
def create_deck():
    name = request.json["name"]
    description = request.json["description"]
    new_deck = Deck(name=name, description=description)
    db.session.add(new_deck)
    db.session.commit()
    return {"response": "ok!"}, status.HTTP_200_OK

@app.route("/my_decks")
def get_decks():
    results = [deck.to_dict() for deck in Deck.query.all()]
    return json.dumps({"results": results}), status.HTTP_200_OK

@app.route("/edit_deck", methods=["PUT"])
def edit_deck():
    id_deck = request.json["id_deck"]
    name = request.json["name"]
    description = request.json["description"]
    deck = Deck.query.filter_by(id_deck=id_deck).first()
    if deck:
        deck.name = name
        deck.description = description
        deck.update_date_now()
        db.session.commit()
        return json.dumps({"results": "ok!"}), status.HTTP_200_OK
    return json.dumps({"results": "id_deck not found!"}), status.HTTP_404_NOT_FOUND

@app.route("/delete_deck", methods=["DELETE"])
def delete_deck():
    id_deck = request.json["id_deck"]
    deck = Deck.query.filter_by(id_deck=id_deck).first()
    if deck:
        db.session.delete(deck)
        db.session.commit()
        return json.dumps({"results":"ok!"}), status.HTTP_200_OK
    return json.dumps({"results":"id_deck not found!"}), status.HTTP_404_NOT_FOUND  

@app.route("/create_card", methods=["POST"])
def create_card():
    front = request.json["front"]
    back = request.json["back"]
    id_deck = request.json["id_deck"]
    new_card = Card(back=back, front=front, id_deck=id_deck)
    db.session.add(new_card)
    db.session.commit()
    return {"response": "ok!"}, status.HTTP_200_OK

@app.route("/my_card", methods=["POST"])    
def get_card():
    id_deck = request.json["id_deck"]
    id_card = request.json["id_card"]
    card = Card.query.filter_by(id_deck=id_deck, id_card=id_card).first()
    if card:
        return json.dumps({"results": card.to_dict()}), status.HTTP_200_OK
    return json.dumps({"results": "id_deck not found!"}), status.HTTP_404_NOT_FOUND

@app.route("/my_cards", methods=["POST"])    
def get_cards():
    id_deck = request.json["id_deck"]
    cards = [card.to_dict() for card in Card.query.filter_by(id_deck=id_deck)]
    if cards:
        return json.dumps({"results": cards}), status.HTTP_200_OK
    return json.dumps({"results": "id_deck not found!"}), status.HTTP_404_NOT_FOUND

@app.route("/edit_card", methods=["PUT"])
def edit_card():
    id_deck = request.json["id_deck"]
    id_card = request.json["id_card"]
    front = request.json["front"]
    back = request.json["back"]
    card = Card.query.filter_by(id_deck=id_deck, id_card=id_card).first()
    if card:
        card.front = front
        card.back = back
        card.update_date_now()
        db.session.commit()
        return json.dumps({"results": "ok!"}), status.HTTP_200_OK
    return json.dumps({"results": "id_deck/id_card not found!"}), status.HTTP_404_NOT_FOUND

@app.route("/delete_card", methods=["POST"])
def delete_card():
    id_deck = request.json["id_deck"]
    id_card = request.json["id_card"]
    card = Card.query.filter_by(id_deck=id_deck, id_card=id_card).first()
    if card:
        db.session.delete(card)
        db.session.commit()
        return json.dumps({"results":"ok!"}), status.HTTP_200_OK
    return json.dumps({"results":"id_deck/id_card not found!"}), status.HTTP_404_NOT_FOUND  

@app.route("/review_cards", methods=["POST"])
def review_cards():
    num_cards_review = 5 # note: i have to put this configuration in a config.ini
    id_deck = request.json["id_deck"]
    cards = [card.to_dict() for card in Card.query.filter_by(id_deck=id_deck)]
    if cards:
        return json.dumps({"results": sorted(cards, key=lambda x: x["grade"])[:num_cards_review]}), status.HTTP_200_OK
    return {"response": "id_deck not found!"}, status.HTTP_404_NOT_FOUND

@app.route("/evaluate_card", methods=["PUT"])
def evaluate_card():
    id_deck = request.json["id_deck"]
    id_card = request.json["id_card"]
    grade = request.json["grade"]
    card = Card.query.filter_by(id_deck=id_deck, id_card=id_card).first()
    if card:
        card.update_grade(grade)
        card.update_last_review()
        db.session.commit()
        return json.dumps({"results":"ok!"}), status.HTTP_200_OK
    return {"response": "card/deck not found!"}, status.HTTP_404_NOT_FOUND


if __name__ == "__main__":
    app.run(debug=True)
    # store_data()