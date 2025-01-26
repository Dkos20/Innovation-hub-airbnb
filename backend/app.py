import os
from flask import flash, redirect, url_for, session
from flask import request
from flask import Flask
from flask_cors import CORS
from functools import wraps
from model.predictor import get_prediction
from data.database import db_session
from data.users import User
from typing import Tuple
from data.database import create_db, DB_CONNECTION_STRING

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SECRET_KEY"] = "SECRET"
app.config['SESSION_TYPE'] = 'filesystem'
DbSession = db_session()


def check_email(email: str) -> bool:
    existing_email = DbSession.query(User).filter(User.email == email).first()
    if not existing_email:
        return True
    return False


def check_username(username: str) -> bool:
    existing_username = DbSession.query(User).filter(User.username == username).first()
    if not existing_username:
        return True
    return False


def check_new_user(email: str, username: str) -> Tuple[int, str]:
    new_email = check_email(email)
    new_username = check_username(username)
    if new_email and new_username:
        return 1, "success"
    if not new_email:
        return 0, "An account with this email already exists"
    if not new_username:
        return 0, "An account with this username already exists"


@app.route('/')
def index():
    return "Airbnb calculator"


@app.route('/register', methods=['GET', 'POST'])
def sign_up():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    if len(username) == 0 or len(email) == 0 or len(password) == 0:
        return 'Some credentials are missing.'
    print("hello")
    status, response = check_new_user(email, username)
    print(f"got email {email}, status = {status}, response = {response}")
    if status:
        new_user = User(username, email, password)
        session['logged_in'] = True
        session.update()
        DbSession.add(new_user)
        DbSession.commit()
    return response


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.json["username"]
        password_candidate = request.json["password"]
        found_user = DbSession.query(User).filter(User.username == username).one()
        if not found_user:
            return "User with this username does not exist"
        if found_user.password == password_candidate:
            session['logged_in'] = True
            session.update()
            return "You are now logged in"
        else:
            return "Wrong password"


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session.keys():
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/calculator', methods=['POST', 'GET'])
# @is_logged_in
def calculator() -> str:
    params = request.json
    prediction = get_prediction(params)
    return str(prediction)


@app.route('/logout')
@is_logged_in
def logout():
    db_session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'secret123'
    db_is_created = os.path.exists(DB_CONNECTION_STRING)
    if not db_is_created:
        create_db()
app.run(host='127.0.0.1', port=5001)
