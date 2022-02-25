from .database import db

class Userdetails(db.Model):
	__tablename__ = 'user_details'
	user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
	username = db.Column(db.String, unique = True)
	active = db.Column(db.Integer, default = 0)
	donecards = db.relationship("Cards", secondary = "user_progress")
	
class Cards(db.Model):
	__tablename__ = 'cards'
	card_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
	language = db.Column(db.String)
	front = db.Column(db.String)
	back = db.Column(db.String)
	finishedusers = db.relationship("Userdetails", secondary = "user_progress")
	
class Deck(db.Model):
	__tablename__ = 'decks'
	Did = db.Column(db.Integer, autoincrement = True, primary_key = True)
	language = db.Column(db.String)

class Userprogress(db.Model):
	__tablename__ = 'user_progress'
	user_id = db.Column(db.Integer, db.ForeignKey("user_details.user_id"), primary_key = True, nullable = False)
	card_id = db.Column(db.Integer, db.ForeignKey("cards.card_id"), primary_key = True, nullable = False)
	marks = db.Column(db.Numeric)
	time = db.Column(db.String)
