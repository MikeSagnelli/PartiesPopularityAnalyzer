from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from forms import SignupForm
import os

app = Flask(__name__)
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

app.secret_key = "development-key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        return "Success!"
    
    elif request.method == 'GET':
        return render_template("signup.html", form=form)

if __name__ == "__main__":
    app.run(debug=True) 