import pickle
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

model1 = pickle.load(open(r'C:\Users\HP\Desktop\malicious\model\malicious.pickle','rb'))  

app = Flask(__name__)
app.config['SECRET_KEY'] = '1233444545555'  # Replace with a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database URI
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create the database tables before running the app
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET'])
def hello():
    return render_template('home.html')
@app.route("/index", methods=['GET'])
def index():
    return render_template('home2.html')

@app.route("/index2", methods=['GET'])
def index2():
    return render_template('index.html')

@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


@app.route("/contact", methods=['GET'])
def contact():
    return render_template('contact.html')



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another username.', 'error')
            return redirect(url_for('signup'))

        # Create a new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('hello'))



@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST': 


        d1 = request.form['url']
        
        arr = np.array([[ d1]])
        print([d1])
        pred1 = model1.predict(arr)[0]

    return render_template('result.html',prediction_text1=pred1)


    
if __name__ == '__main__':
    app.run(debug=True)
    
