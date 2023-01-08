from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    done = db.Column(db.Boolean)
    active = db.Column(db.Boolean)


db.create_all()


@app.get("/")
def home():
    todos = db.session.query(Todo).all()
    return render_template("base.html", todos=todos)


@app.post("/add")
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, done=False, active=True)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/activate/<int:todo_id>")
def activate(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.active = True
    db.session.commit()
    return redirect(url_for("home"))

@app.get("/deactivate/<int:todo_id>")
def deactivate(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.active = False
    db.session.commit()
    return redirect(url_for("home"))



@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))
