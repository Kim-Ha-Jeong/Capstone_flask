from flask import Flask, jsonify, Blueprint
from flask_restful import reqparse
from database import *

user_api = Blueprint('user_api', __name__)


@user_api.route('/user', methods=['POST'])
def user_create():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    args = parser.parse_args()

    email = args['email']
    password = args['password']

    engine.execute("insert into user (email,password) values (%s, %s)", email, password)

    return {'email': email, 'password': password}


@user_api.route('/user', methods=['GET'])
def user_list():
    result = engine.execute("select * from user")

    return jsonify([dict(row) for row in result]);
