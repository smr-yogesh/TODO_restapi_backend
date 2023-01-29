from flask import Flask
from utils.db import db

app = Flask(__name__)                                  #user   #password         #database
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:password@localhost/tododb'
app.config["SECRET_KEY"] = 'thisisthekey'

db.init_app(app)