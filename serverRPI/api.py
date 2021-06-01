import os
import sys
from serverRPI.helper import Ordre

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_cors import CORS

from time import sleep

#from serverRPI.rover import Rover

app = Flask(__name__)
app.config['CORS_HEADERS'] = '*'

CORS(app, origins="*", allow_headers="*")
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
#rover = Rover()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    rank = db.Column(db.Integer)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



@app.route('/', methods=['GET'])
def get_home():
    return jsonify({'Title':{'message':'API EINSTEIN - rovEr Institu uNiverSitaire TEchnologIe lyoN'}})


#----------------------------------------- SECURITY ------------------------------
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})



#----------------------------------------- USER ------------------------------
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if current_user.rank!=0:
        return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['rank'] = user.rank
        output.append(user_data)

    return jsonify({'users' : output})


#----------------------------------------- ROVER ------------------------------
@app.route('/rover/<int:value>', methods=['GET'])
@token_required
def avancer(current_user,value):
    #Exemple de controle de value
    if value > 0 and value<200:
        pass #rover.avancer(Ordre.AV,value)
        return jsonify({'Order' : "Apply"})
    else:
        return jsonify({'Order':'Error', 'message':'Value error'})

@app.route('/stop', methods=['GET'])
@token_required
def stop(current_user):
    return jsonify({'Order': "Apply"})
    pass#rover.arreter(Ordre.OFF)



if __name__ == '__main__':

    if not os.path.exists('db.sqlite'):
        db.create_all()
        u = User(name="admin")
        u.password = generate_password_hash("azerty")
        u.rank = 0
        db.session.add(u)
        db.session.commit()
    app.run(host="0.0.0.0",port=8123,debug=True)