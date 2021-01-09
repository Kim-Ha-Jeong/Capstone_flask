from flask import Blueprint, jsonify, render_template
from flask_login import login_user, current_user, login_required
from flask_restful import reqparse
from src.database import engine

login_api = Blueprint('login_api', __name__)

class User:
    def __init__(self, user_id=None, email=None, password=None, authenticated=True):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.authenticated = authenticated

    def __repr__(self):
        r = {
            'user_id': self.user_id,
            'email': self.email,
            'password': self.password,
            'authenticated': self.authenticated,
        }
        return str(r)

    def can_login(self, password):
        return self.password == password

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


result2 = engine.execute("select * from user")
USERS = {}
for row in result2:
    USERS.update({row[0] : User(user_id=row[0],email=row[1], password=row[2]) })


@login_api.route('/login', methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    args = parser.parse_args()

    email = args['email']
    password = args['password']

    result = engine.execute("select id from user where email=%s and password=%s", email, password)

    for row in result:
        uid = row['id']

    login_user(USERS[uid], remember=True)
    return "ok"


@login_api.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@login_api.route('/logout', methods=['POST'])
def logout():
    user = current_user
    user.authenticated = False
    json_res = {'ok': True, 'msg':'user <%s> logout' %user.user_id}
    return jsonify(json_res)

