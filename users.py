from flask import Flask, jsonify, Blueprint, request, session, render_template, redirect
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

    return render_template('user.html', datas=result)


@user_api.route('/user/<id>', methods=['POST'])
def update(id):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    args = parser.parse_args()

    email = args['email']
    password = args['password']

    engine.execute("update user set email=%s,password=%s where id=%s", email, password, id)
    return redirect("/api/user")


@user_api.route('/user/<id>', methods=['GET'])
def show(id):
    result = engine.execute("select * from user where id=%s",id)

    return render_template('user_update.html', datas=result)


@user_api.route('/user/delete/<id>', methods=['GET'])
def delete(id):
    engine.execute("delete from user where id=%s", id)
    return redirect("/api/user")