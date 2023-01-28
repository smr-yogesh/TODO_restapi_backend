from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
from functools import wraps

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:password@localhost/tododb'
app.config["SECRET_KEY"] = 'thisisthekey'
db=SQLAlchemy(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify ({'message':'Token is required!'}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"],algorithms='HS256')
            user = User.query.filter_by(email=data['user']).first()
        except:
            return jsonify({'message':'Invalid token'}), 401
        return f(user,*args, **kwargs)
    return decorated
#Model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), unique=True)
    pswd = db.Column(db.String(255))
    created = db.Column(db.DateTime(), default = datetime.utcnow)
    updated = db.Column(db.DateTime(), default = datetime.utcnow)

    def __init__(self,email,pswd, updated):
       self.email= email
       self.pswd = generate_password_hash(pswd, method='sha256')
       self.updated = updated

class status:
    NOTSTARTED = 'NotStarted'
    ONGOING = 'OnGoing'
    COMPETED = 'Completed'

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    created = db.Column(db.DateTime(), default = datetime.utcnow)
    updated = db.Column(db.DateTime(), default = datetime.utcnow)
    status = db.Column(db.Enum("NotStarted","OnGoing","Completed", name="status"), default = "NotStarted")

    def __init__(self,name,description,uid, created, updated,status):
       self.name = name
       self.description = description
       self.user_id = uid
       self.created = created
       self.updated = updated
       self.status = status


@app.route('/api/v1/signup', methods = ['POST'])
def signup():
    data = request.get_json()
    email = data["email"]
    pswd = data["password"]
    update_time = data["update_time"]
    user = User(email,pswd,update_time)
    db.session.add(user)
    db.session.commit()
    return data

@app.route('/api/v1/sigin', methods = ['POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.pswd, password):
            token = jwt.encode({'user': email, 'exp' : datetime.utcnow() + timedelta(minutes= 5)}, app.config["SECRET_KEY"], algorithm='HS256')
            return jsonify({'token':token.encode().decode('utf-8')})
        else :
            return jsonify({'message':'Invalid password'})

@app.route('/api/v1/changePassword', methods = ['PUT','GET'])
@token_required
def changepassword(user):
    email = user.email
    newpass = generate_password_hash(request.get_json()['password'])
    if newpass:
        User.query.filter_by(email = email).update(dict(pswd=newpass))
        db.session.commit()
        return jsonify ({'message': 'Password changed successfully!!'})
    


@app.route('/api/v1/todos?status=', methods = ['GET'])
@token_required
def todos_s():
    allusers= Todo.query.all()
    output = []
    for result in allusers:
        nowuser = {}
        nowuser['id'] = result.id
        nowuser['email'] = result.email
        nowuser['created'] = result.created
        output.append(nowuser)
    return jsonify(output)

@app.route('/api/v1/todos', methods = ['POST','GET'])
@token_required
def createTodo():
    return

@app.route('/api/v1/todos/:id', methods = ['PUT'])
@token_required
def updateTodo():
    return

@app.route('/api/v1/todos/:id', methods = ['DELETE'])
@token_required
def delTodo():
    return

if __name__ == '__main__':
    app.run(debug=True)