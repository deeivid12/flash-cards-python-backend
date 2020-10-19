from models import models
from flask import Flask, request, jsonify
from flask_api import status
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

all_decks_db = list()

app = Flask(__name__)

@app.route("/create_deck", methods=["POST"])
def create_deck():
    name = request.json["name"]
    description = request.json["description"]
    new_deck = models.Deck(name, description)
    all_decks_db.append(new_deck)
    return {"response":"ok!"}, status.HTTP_200_OK
    
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

@app.route("/create_card", methods=["POST"])
def create_card():
    front = request.json["front"]
    back = request.json["back"]
    id_deck = request.json["id_deck"]
    for deck in all_decks_db:
        if id_deck == deck.id_deck:
            new_card = models.Card(front, back, id_deck)
            deck.add_card(new_card)
            return {"response":"ok!"}, status.HTTP_200_OK
    return {"response":"id_deck not found!"}, status.HTTP_404_NOT_FOUND

@app.route("/my_cards", methods=["POST"])    
def get_all_cards_from_deck():
    id_deck = request.json["id_deck"]
    for deck in all_decks_db:
        if id_deck == deck.id_deck:
            results = [card.to_dict() for card in deck.cards]
            return json.dumps({"results": results}), status.HTTP_200_OK
    return {"response":"id_deck not found!"}, status.HTTP_404_NOT_FOUND
            

if __name__ == "__main__":
    app.run(debug=True)
    