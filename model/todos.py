from utils.db import db
from datetime import datetime

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