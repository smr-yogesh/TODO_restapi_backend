from utils.db import db
from routes import app
from routes.todo_routes import B_todo
from routes.user_routes import B_user

app.register_blueprint(B_todo)
app.register_blueprint(B_user)

app.app_context().push()
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)