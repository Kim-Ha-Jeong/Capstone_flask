from flask import Blueprint, session
from flask_restful import reqparse

from src.database import engine

login_api = Blueprint('login_api', __name__)


@login_api.route('/login', methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    args = parser.parse_args()

    email = args['email']
    password = args['password']

    result = engine.execute("select * from user where email=%s and password=%s", email, password)

    if result is not None:
        session['logged_in'] = True
        return "Success"
    else:
        return "Can't login"


@login_api.route('/logout')
def logout():
    session['logged_in'] = False
    return 'logout'
