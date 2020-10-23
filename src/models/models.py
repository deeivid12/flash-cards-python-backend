import datetime
import copy

class Deck():
    id_deck = 0
    recently_created = True
    reviews_today = 0
    reviews_per_day = 0
    total_reviews = 0
        
    def __init__(self, name, description):
        Deck.id_deck += 1
        self.id_deck = Deck.id_deck
        self.name = name
        self.description = description
        self.creation_date = datetime.datetime.now()
        self.update_date = copy.deepcopy(self.creation_date)
        self.status = "active" # active, hidden, delete?
        self.cards = []
    
    def add_card(self, card):
        if isinstance(card, Card):
            self.cards.append(card)
            self.update_date_now()
            
    def remove_card(self, card):
        if isinstance(card, Card):
            if card in self.cards:
                self.cards.remove(card)
                self.update_date_now()
                
    def to_dict(self):
      return {"id_deck": self.id_deck ,"name": self.name, "description": self.description,
              "creation_date": self.creation_date.__str__(), "status": self.status,
              "update_date": self.update_date.__str__()}
      
    def update_date_now(self):
        self.update_date = datetime.datetime.now()
        if self.recently_created:
            self.recently_created = False
            
        
        
class Card():
    id_card = 0
    num_reviews = 0
    grade = 0 # fail, hard, good, easy
    recently_created = True
    last_review = None
    #box = 1
    
    def __init__(self, front, back, id_deck, tags=None):
        Card.id_card += int(1)
        self.id_card = Card.id_card
        self.id_deck = id_deck
        self.front = front
        self.back = back
        self.creation_date = datetime.datetime.now()
        self.update_date = copy.deepcopy(self.creation_date)
        if(tags is None):
            self.tags = []
        else:
            self.tags = tags
            
    def to_dict(self):
        return { "id_card": self.id_card, "front": self.front,
                 "back": self.back, "id_deck": self.id_deck,
                 "grade": self.grade, "update_date": self.update_date.__str__(),
                 "creation_date": self.creation_date.__str__(), "last_review": self.last_review.__str__()}
        
    def update_grade(self, grade):
        self.grade = grade
        
    def update_date_now(self):
        self.update_date = datetime.datetime.now()
        if self.recently_created:
            self.recently_created = False
            
    def update_last_review(self):
        self.last_review = datetime.datetime.now()

"""
if __name__ == "__main__":
    deck1 = Deck("Lesson 2 B1", "Lesson from B1 certificate")
    print(deck1.creation_date)
    print(deck1.status)
    
"""
        
        


        
        
        


    