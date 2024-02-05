from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# config: a dictionary (as mentioned by the video tutorial) which stores manage setup variables
# /// means relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # create the actual database

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # for each entry we create a column, want to have unique keys
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    
@app.route('/')
def index():
    # show all todos
    todo_list =  Todo.query.all()
    #print(todo_list)
    return render_template('base.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            new_todo = Todo(title="todo 1", complete=False)
            db.session.add(new_todo)
            db.session.commit()
        except Exception as e:
            print(f"An error occurred while creating the database: {e}")


    app.run(debug=True)



# # only use a forward slash /because this is going to be our start page.
# @app.route("/")
# def home():
#     todo_list = Todo.query.all()
#     return render_template("base.html", todo_list=todo_list)

# # if we go to /add, we see content defined by the add function
# @app.route("/add", methods=["POST"])
# def add():
#     title = request.form.get("title")
#     new_todo = Todo(title=title, complete=False)
#     db.session.add(new_todo)
#     db.session.commit()
#     return redirect(url_for("home"))

# # similarly
# @app.route("/update/<int:todo_id>")
# def update(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()
#     todo.complete = not todo.complete
#     db.session.commit()
#     return redirect(url_for("home"))


# @app.route("/delete/<int:todo_id>")
# def delete(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()
#     db.session.delete(todo)
#     db.session.commit()
#     return redirect(url_for("home"))