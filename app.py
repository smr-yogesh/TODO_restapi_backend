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

    def __init__(self,name,description,uid, updated,status):
       self.name = name
       self.description = description
       self.user_id = uid
       self.updated = updated
       self.status = status
app.app_context().push()
db.create_all()
#signup
@app.route('/api/v1/signup', methods = ['POST'])
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
@app.route('/api/v1/sigin', methods = ['POST'])
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
@app.route('/api/v1/changePassword', methods = ['PUT'])
@token_required
def changepassword(user):
    updated = datetime.utcnow()
    email = user.email
    newpass = generate_password_hash(request.get_json()['password'])
    if newpass:
        User.query.filter_by(email = email).update(dict(pswd=newpass, updated = updated))
        db.session.commit()
        return jsonify ({'message': 'Password changed successfully!!'})
    

#get todos
@app.route('/api/v1/todos', methods = ['GET'])
@token_required
def todos_s(user):
    uid = user.id
    status = request.args.get('status')
    todos= Todo.query.filter_by(status=status, user_id = uid)
    output = []
    for result in todos:
        todo = {}
        todo['name'] = result.name
        todo['description'] = result.description
        todo['status'] = result.status
        todo['created'] = result.created
        todo['updated'] = result.updated
        output.append(todo)
    return jsonify(output)

#create todo
@app.route('/api/v1/todos', methods = ['POST'])
@token_required
def createTodo(user):
    data = request.get_json()
    name = data['name']
    desc = data['description']
    uid = user.id
    updated = datetime.utcnow()
    status = "NotStarted"
    todo = Todo(name=name,description=desc,uid=uid,updated=updated,status=status)
    db.session.add(todo)
    db.session.commit()


@app.route('/api/v1/todos/<id>', methods = ['PUT'])
@token_required
def updateTodo(user,id):
    data = request.get_json()
    uid = user.id
    todo_id = id
    old_data = Todo.query.filter_by(id=todo_id, user_id = uid).first()
    name = data['name']
    desc = data['description']
    status = data['status']
    updated = datetime.utcnow()
    try :
        if name == '': name = old_data.name
        if desc == '': desc = old_data.description
        if status == '' : status = old_data.status
        Todo.query.filter_by(id=todo_id, user_id = uid).update(dict(name=name,description=desc,updated=updated,status=status))
        db.session.commit()
    except :
        return jsonify ({'message':'Not allowed'}),403  

    return jsonify ({'message':'Todo edited sucessfully'})

@app.route('/api/v1/todos/<id>', methods = ['DELETE'])
@token_required
def delTodo(user,id):
    uid = user.id
    todo_id = int(id)
    todos = Todo.query.filter_by(user_id = uid)
    ids = []
    for each in todos:
        ids.append(each.id)
    if todo_id in ids:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
        return jsonify ({'message':'Todo deleted sucessfully'})
    else:
        return jsonify ({'message':'Not allowed'}),403  

if __name__ == '__main__':
    app.run(debug=True)