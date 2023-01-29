from routes import app
from flask import request, jsonify, Blueprint
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from auth import token_required
import jwt 
from model.users import User
from utils.db import db
B_user = Blueprint('B_user', __name__)
@B_user.route('/api/v1/signup', methods = ['POST'])
def signup():
    data = request.get_json()
    email = data["email"]
    pswd = data["password"]
    updated = datetime.utcnow()
    user = User(email,pswd,updated)
    db.session.add(user)
    db.session.commit()
    return data

#signin
@B_user.route('/api/v1/sigin', methods = ['POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.pswd, password):
            token = jwt.encode({'user': email, 'exp' : datetime.utcnow() + timedelta(minutes= 30)}, app.config["SECRET_KEY"], algorithm='HS256')
            return jsonify({'token':token.encode().decode('utf-8')})
        else :
            return jsonify({'message':'Invalid password'})

#Change user passwords
@B_user.route('/api/v1/changePassword', methods = ['PUT'])
@token_required
def changepassword(user):
    updated = datetime.utcnow()
    email = user.email
    newpass = generate_password_hash(request.get_json()['password'])
    if newpass:
        User.query.filter_by(email = email).update(dict(pswd=newpass, updated = updated))
        db.session.commit()
        return jsonify ({'message': 'Password changed successfully!!'})
    