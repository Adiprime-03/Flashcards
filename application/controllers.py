from flask import Flask
from flask import render_template as rt
from flask import request
from werkzeug.utils import redirect
from datetime import datetime as dt
from flask import current_app as app
from logging import exception

from application.models import Userdetails, Cards, Deck, Userprogress
from application.database import db

@app.route("/")
def start():
  return rt('home.html', err = "")

@app.route("/login", methods =["GET", "POST"])
def login():
	if(request.method == "GET"):
		return rt('login.html', err ="")
	elif(request.method == "POST"):
		user_name = request.form["user_name"]
		if(user_name == ""):
			return rt('login.html', err = "*Enter something")
		users = Userdetails.query.all()
		usernames = []
		for user in users:
			usernames.append(user.username)
		if(user_name in usernames):
			u = Userdetails.query.filter(Userdetails.username == user_name).first()
			u.active = 1
			db.session.commit()
			return redirect(f"/dashboard/{user_name}")
		else:
			return rt('login.html', err = "*This username doesn't exist")
	else:
		raise exception("Method unknown")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
	if(request.method == "GET"):
		return rt('signup.html', err = "")
	elif(request.method == "POST"):
		user_name = request.form["user_name"]
		if(user_name == ""):
			return rt('login.html', err = "*Enter something")
		users = Userdetails.query.all()
		usernames = []
		for user in users:
			usernames.append(user.username)
		if(user_name in usernames):
			return rt('signup.html', err = "*This username already exists. Pick a new one!")
		user = Userdetails(username = user_name)
		db.session.add(user)
		db.session.commit()
		return redirect("/login")
	else:
		raise exception("Method unknown")

@app.route("/dashboard/<user_name>")
def dashboard(user_name):
	def time(ftime, ptime):
		if(dt.strptime(str(ftime.value), '%y/%m/%d %H:%M:%S')> dt.strptime(str(ptime), '%y/%m/%d %H:%M:%S')):
			return ftime.value
		else:
			return ptime
	
	def floatify(Score):
		return round(float(Score), 2)
	
	
	user = Userdetails.query.filter(Userdetails.username == user_name).all()
	u = Userdetails.query.filter(Userdetails.username == user_name).first()
	if(u.active == 0):
		return redirect("/login")
	decks = Deck.query.all()
	userid = user[0].user_id
	progress = Userprogress.query.filter(Userprogress.user_id == userid).all()
	arg = 1
	if(len(progress)==0):
		arg = 0
	return rt('dashboard.html', user = user, decks = decks, progress = progress, arg = arg, time = time, floatify = floatify)

@app.route("/question/<user_name>/<lang>", methods = ["GET", "POST"])
def question(user_name, lang):
	u = Userdetails.query.filter(Userdetails.username == user_name).first()
	if(u.active == 0):
		return redirect("/login")
	n = int(request.args.get('n'))
	user = Userdetails.query.filter(Userdetails.username == user_name).all()
	userid = user[0].user_id
	qcards = Cards.query.filter(Cards.language == lang).all()
	finalcards = []
	for qc in qcards:
		finalcards.append(qc)
	l = len(finalcards)

	return rt('question.html', finalcards = finalcards, user = user, n = n, l = l, lang = lang)

@app.route("/viewdeck")
def viewdeck():
	decks = Deck.query.all()
	cards = Cards.query.all()
	return rt('viewdeck.html', decks = decks, cards = cards)

@app.route("/addtodeck/<LANGUAGE>", methods = ["GET", "POST"])
def addtodeck(LANGUAGE):
	if(request.method == "GET"):
		return rt('addtodeck.html', LANGUAGE = LANGUAGE)
	elif(request.method == "POST"):
		FRONT = request.form["FRONT"]
		BACK = request.form["BACK"]
		c = Cards(language = LANGUAGE, front = FRONT, back = BACK)
		db.session.add(c)
		db.session.commit()
		return redirect('/viewdeck')
	else:
		print("Error")
	
@app.route("/adddeck", methods = ["GET", "POST"])
def adddeck():
    if(request.method == "GET"):
        return rt('adddeck.html', err = "")
    elif(request.method == "POST"):
        LANGUAGE = request.form["LANGUAGE"]
        if(LANGUAGE == ""):
            return rt('adddeck.html', err = "Enter something!")
        ds = Deck.query.filter(Deck.language == LANGUAGE).all()
        for d in ds:
            if(LANGUAGE == d.language):
                return rt('adddeck.html', err = "Deck is already added")
        c = Deck(language = LANGUAGE)
        db.session.add(c)
        db.session.commit()
        return redirect('/viewdeck')
    else:
        print("Error")

@app.route("/progress/<userid>/<cardid>/<mark>")
def updateprogress(userid, cardid, mark):
	print("invoked", userid, cardid, mark)
	now = dt.now()
	givencardprogress = Userprogress.query.filter((Userprogress.user_id == userid) & (Userprogress.card_id == cardid)).first()
	if(givencardprogress == None):
		givencardprogress = Userprogress(user_id = int(userid), card_id = int(cardid), marks = int(mark), time = now.strftime("%y/%m/%d %H:%M:%S"))
		db.session.add(givencardprogress)
		db.session.commit()
	else:
		givencardprogress.marks = mark
		givencardprogress.time = now.strftime("%y/%m/%d %H:%M:%S")
		db.session.commit()
	return "OK", 200

@app.route("/logout/<userid>")
def logout(userid):
	u = Userdetails.query.filter(Userdetails.user_id == userid).first()
	u.active = 0
	db.session.commit()
	next = str(request.args.get('next'))
	if next == "login":
		return redirect('/login')
	elif next == "view":
		return redirect('/viewdeck')
	elif next == "add":
		return redirect('/adddeck')

