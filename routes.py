# -*- coding: utf-8 -*-
from __future__ import division
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from flask_pymongo import PyMongo
from forms import SignupForm, LoginForm, AdminForm, CandidatesForm
from models import User
from utils import TwitterAPI, SentimentAnalyzer, Queries
from werkzeug import check_password_hash
import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)
analyzer = SentimentAnalyzer()
twitter_api = TwitterAPI()

app.secret_key = 'development-key'

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('home'))
    else:
        return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' not in session:
        form = SignupForm()

        if request.method == 'POST':
            if form.validate() == False:
                return render_template('signup.html', form=form)
            else:
                users = mongo.db.users
                user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
                users.insert({
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "pwd_hash": user.pwd_hash,
                    "role": "user"
                })

                session['email'] = user.email
                session['first_name'] = user.first_name
                session['last_name'] = user.last_name
                session['role'] = "user"
                return redirect(url_for('home'))
        
        elif request.method == 'GET':
            return render_template('signup.html', form=form)
    else:
        return redirect(url_for('home'))

@app.route('/createAdmin', methods=['GET', 'POST'])
def create_admin():
    if 'role' in session and session['role'] == 'admin':
        form = SignupForm()

        if request.method == 'POST':
            if form.validate() == False:
                return render_template('signup.html', form=form)
            else:
                users = mongo.db.users
                user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
                users.insert({
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "pwd_hash": user.pwd_hash,
                    "role": 'admin'
                })
                return redirect(url_for('home'))
        
        elif request.method == 'GET':
            return render_template('signup.html', form=form)
    elif 'role' in session and session['role'] == 'user':
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if 'email' not in session:
        form = LoginForm()

        if request.method == "POST":
            if form.validate() == False:
                return render_template("login.html", form=form)
            else:
                email = form.email.data
                password = form.password.data

                users = mongo.db.users
                user = users.find_one({"email": email})
                if user is not None and check_password_hash(user['pwd_hash'], password):
                    session['email'] = form.email.data
                    session['first_name'] = user['first_name']
                    session['last_name'] = user['last_name']
                    session['role'] = user['role']
                    if user['role'] == 'admin':
                        return redirect(url_for('admin'))
                    else:
                        return redirect(url_for('home'))
                else:
                    return redirect(url_for('login'))
        elif request.method == "GET":
            return render_template('login.html', form=form)
    else:
        return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route("/admin", methods=['GET','POST'])
def admin():
    if 'role' in session and session['role'] == 'admin':
        form = AdminForm()
        if request.method == "GET":
            title = 'Admin'
            return render_template('admin.html', form=form, title=title)
        
        elif request.method == "POST":
            queries = Queries.get_queries()
            if form.states.data == 'All':
                cursor = mongo.db.locations.find({})
            else:
                cursor = mongo.db.locations.find({'state': form.states.data})
            for document in cursor:
                for candidate, query in queries:
                    query.encode('utf-8')
                    max_tweets = 50
                    searched_tweets = []
                    last_id = -1
                    while len(searched_tweets) < max_tweets:
                        count = max_tweets - len(searched_tweets)
                        try:
                            new_tweets = twitter_api.api.search(q=query, count=count, max_id=str(last_id - 1), geocode=document['geocode'])
                            if not new_tweets:
                                break
                            searched_tweets.extend(new_tweets)
                            last_id = new_tweets[-1].id
                        except twitter_api.tweepy.TweepError as e:
                            print(e)
                            break
                    count = 0
                    accum = 0
                    for t in searched_tweets:
                        if not t.retweeted and 'RT @' not in t.text and t.lang == 'es':
                            sentiment = analyzer.analyze_sentiment(t.text)
                            if sentiment >= 0.15 and sentiment <= 0.85:
                                count+=1
                                accum+=sentiment
                    try:
                        average = accum / count
                    except ZeroDivisionError:
                        average = 0
                    mongo.db.analyzed_tweets.insert({
                        "candidate": candidate,
                        "state": document['state'],
                        "sentiment": average
                    })
            return redirect(url_for('admin'))

    elif 'role' in session and session['role'] == 'user':
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    

@app.route("/home")
def home():
    if 'role' in session and session['role'] == 'admin':
        return redirect(url_for('admin'))
    else:
        if 'email' in session:
            title = 'Home'
            return render_template("home.html", title=title)
        else:
            return redirect(url_for('login'))

@app.route("/map", methods=['GET', 'POST'])
def map():
    if 'email' in session:
        title = 'Map Analyzer'
        candidates = {
            'AMLO': 'Andrés Manuel López Obrador',
            'Anaya': 'Ricardo Anaya Cortés',
            'Meade': 'José Antonio Meade Kuribeña',
            'Zavala': 'Margarita Ester Zavala Gómez del Campo',
            'Bronco': 'Jaime Rodríguez Calderón'
        }
        images = [
            url_for('static', filename = 'img/amlo.jpg'),
            url_for('static', filename = 'img/anaya.jpg'),
            url_for('static', filename = 'img/meade.jpg'),
            url_for('static', filename = 'img/zavala.jpg'),
            url_for('static', filename = 'img/bronco.jpg')
        ]
        form = CandidatesForm()
        if request.method == "GET":
            analyzed = 'AMLO'
            cursor = mongo.db.analyzed_tweets.find({'candidate': analyzed})
            loc_sentiment = {}
            for document in cursor:
                loc_sentiment[document['state']] = document['sentiment'] * 100
            return render_template('map.html', form=form, title=title, images=images, analyzed=analyzed, candidate_name=candidates[analyzed], loc_sentiment=loc_sentiment)
        elif request.method == "POST":
            analyzed = form.candidates.data
            cursor = mongo.db.analyzed_tweets.find({'candidate': analyzed})
            loc_sentiment = {}
            for document in cursor:
                loc_sentiment[document['state']] = document['sentiment'] * 100
            return render_template('map.html', form=form, title=title, images=images, analyzed=analyzed, candidate_name=candidates[analyzed], loc_sentiment=loc_sentiment)
    else:
        return redirect(url_for('login'))

@app.route("/overview")
def overview():
    if 'email' in session:
        title = 'Map Overview'
        candidates = {
            'AMLO': 'Andrés Manuel López Obrador',
            'Anaya': 'Ricardo Anaya Cortés',
            'Meade': 'José Antonio Meade Kuribeña',
            'Zavala': 'Margarita Ester Zavala Gómez del Campo',
            'Bronco': 'Jaime Rodríguez Calderón'
        }
        states=['Aguascalientes',
        'Baja California',
        'Baja California Sur',
        'Campeche',
        'Chiapas',
        'Chihuahua',
        'Ciudad de México',
        'Coahuila',
        'Colima',
        'Durango',
        'Guanajuato',
        'Guerrero',
        'Hidalgo',
        'Jalisco',
        'México',
        'Michoacán',
        'Morelos',
        'Nayarit',
        'Nuevo León',
        'Oaxaca',
        'Puebla',
        'Querétaro',
        'Quintana Roo',
        'San Luis Potosí',
        'Sinaloa',
        'Sonora',
        'Tabasco',
        'Tamaulipas',
        'Tlaxcala',
        'Veracruz',
        'Yucatán',
        'Zacatecas']
        images = [
            url_for('static', filename = 'img/amlo.jpg'),
            url_for('static', filename = 'img/anaya.jpg'),
            url_for('static', filename = 'img/meade.jpg'),
            url_for('static', filename = 'img/zavala.jpg'),
            url_for('static', filename = 'img/bronco.jpg')
        ]

        amlo = mongo.db.analyzed_tweets.find({'candidate': 'AMLO'})
        amlo_sentiment = {}
        for document in amlo:
            amlo_sentiment[document['state'].encode('utf-8')] = document['sentiment'] * 100

        anaya = mongo.db.analyzed_tweets.find({'candidate': 'Anaya'})
        anaya_sentiment = {}
        for document in anaya:
            anaya_sentiment[document['state'].encode('utf-8')] = document['sentiment'] * 100
        

        meade = mongo.db.analyzed_tweets.find({'candidate': 'Meade'})
        meade_sentiment = {}
        for document in meade:
            meade_sentiment[document['state'].encode('utf-8')] = document['sentiment'] * 100
        

        zavala = mongo.db.analyzed_tweets.find({'candidate': 'Zavala'})
        zavala_sentiment = {}
        for document in zavala:
            zavala_sentiment[document['state'].encode('utf-8')] = document['sentiment'] * 100
        

        bronco = mongo.db.analyzed_tweets.find({'candidate': 'Bronco'})
        bronco_sentiment = {}
        for document in bronco:
            bronco_sentiment[document['state'].encode('utf-8')] = document['sentiment'] * 100

        analyzed = 'AMLO'

        loc_winner = {}
        loc_sentiment = {}
        for state in states:
            winner = 'AMLO'
            sentiment_winner = amlo_sentiment[state]
            if anaya_sentiment[state] > sentiment_winner:
                sentiment_winner = anaya_sentiment[state]
                winner = 'Anaya'
            if meade_sentiment[state] > sentiment_winner:
                sentiment_winner = meade_sentiment[state]
                winner = 'Meade'
            if zavala_sentiment[state] > sentiment_winner:
                sentiment_winner = zavala_sentiment[state]
                winner = 'Zavala'
            if bronco_sentiment[state] > sentiment_winner:
                sentiment_winner = bronco_sentiment[state]
                winner = 'Bronco'

            loc_winner[state] = winner
            loc_sentiment[state] = sentiment_winner
            
        return render_template('overview.html', title=title, images=images, candidates=candidates, loc_winner=loc_winner, loc_sentiment=loc_sentiment)
    else:
        return redirect(url_for('login'))

@app.route("/feedback")
def feedback():
    if 'email' in session:
        title = 'Feedback'
        return render_template('feedback.html', title=title)
    else:
        return redirect(url_for('login'))

@app.route("/responses")
def responses():
    if 'role' in session and session['role'] == 'admin':
        title = 'Responses'
        return render_template('responses.html', title=title)
    else:
        if 'email' in session:
            title = 'Home'
            return render_template("home.html", title=title)
        else:
            return redirect(url_for('login'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'), 'favicon.ico', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)    