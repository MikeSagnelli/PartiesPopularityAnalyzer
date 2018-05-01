from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from forms import SignupForm, LoginForm
from models import User
from werkzeug import check_password_hash
import os

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

app.secret_key = 'development-key'

@app.route('/')
def index():
    form = SignupForm()
    if 'email' in session:
        return redirect(url_for('home'))
    else:
        return render_template('index.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
                "pwd_hash": user.pwd_hash
            })

            session['email'] = user.email
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            return redirect(url_for('home'))
    
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
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
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    elif request.method == "GET":
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    return redirect(url_for('index'))

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True) 