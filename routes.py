from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from forms import SignupForm
from models import User
import os

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

app.secret_key = 'development-key'

@app.route('/')
def index():
    return render_template('index.html')

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
            return redirect(url_for('home'))
    
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True) 