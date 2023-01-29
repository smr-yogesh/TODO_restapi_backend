from flask import request, jsonify, Blueprint
from datetime import datetime
from auth import token_required
from model.todos import Todo
from utils.db import db

B_todo = Blueprint('B_todo', __name__)
@B_todo.route('/api/v1/todos', methods = ['GET'])
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
@B_todo.route('/api/v1/todos', methods = ['POST'])
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


@B_todo.route('/api/v1/todos/<id>', methods = ['PUT'])
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

@B_todo.route('/api/v1/todos/<id>', methods = ['DELETE'])
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