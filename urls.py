from flask_restful import reqparse, Api
from flask import Flask, jsonify
from database import *

app = Flask(__name__)
api = Api(app)


@app.route('/user', methods=['POST'])
def sign_up():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    args = parser.parse_args()

    email = args['email']
    password = args['password']

    engine.execute("insert into users (email,password) values (%s, %s)", email, password)

    return {'email': email, 'password': password}


@app.route('/user', methods=['GET'])
def user_list():
    result = engine.execute("select * from users")

    return jsonify([dict(row) for row in result]);

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST':



if __name__ == '__main__':
    app.run(debug=True)
