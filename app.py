from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    review = db.Column(db.String(144))

    def __init__(self, title, author, review):
        self.title = title
        self.author = author
        self.review = review

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "author", "review")

book_schema = BookSchema()
multiple_book_schema = BookSchema(many=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    books = ...

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)


@app.route("/book/add", methods=["POST"])
def add_book():
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    post_data = request.get_json()
    title = post_data.get("title")
    author = post_data.get("author")
    review = post_data.get("review")

    record = Book(title, author, review)
    db.session.add(record)
    db.session.commit()

    return jsonify("Book added successfully")

@app.route("/book/get", methods=["GET"])
def get_all_books():
    all_books = db.session.query(Book).all()
    return jsonify(multiple_book_schema.dump(all_books))

@app.route("/book/get/<id>", methods=["GET"])
def get_one_book(id):
    book = db.session.query(Book).filter(Book.id == id).first()
    return jsonify(book_schema.dump(book))

@app.route("/book/update/<id>", methods=["PUT"])
def update_book(id):
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    put_data = request.get_json()
    title = put_data.get("title")
    author = put_data.get("author")
    review = put_data.get("review")

    book = db.session.query(Book).filter(Book.id == id).first()
    if book is None:
        return jsonify(f"Error: book with id of {id} doesn't exist.")

    if title:
        book.title = title
    if author:
        book.author = author
    if review:
        book.review = review

    db.session.commit()

    return jsonify("Book updated successfully")
    
@app.route("/book/update/title/<book_title>", methods=["PUT"])
def update_book_by_title(book_title):
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    put_data = request.get_json()
    title = put_data.get("title")
    author = put_data.get("author")
    review = put_data.get("review")

    book = db.session.query(Book).filter(Book.title == book_title).first()
    if book is None:
        return jsonify(f"Error: book with title of {book_title} doesn't exist.")

    if title:
        book.title = title
    if author:
        book.author = author
    if review:
        book.review = review

    db.session.commit()

    return jsonify("Book updated successfully")

@app.route("/book/delete/<id>", methods=["DELETE"])
def delete_book(id):
    book = db.session.query(Book).filter(Book.id == id).first()
    db.session.delete(book)
    db.session.commit()
    return jsonify("Book deleted successfully")

@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    record = User(username, password)
    db.session.add(record)
    db.session.commit()

    return jsonify("User added successfully")

@app.route("/user/get", methods=["GET"])
def get_all_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))

@app.route("/user/get/<id>", methods=["GET"])
def get_one_user(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/update/<id>", methods=["PUT"])
def update_user(id):
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    put_data = request.get_json()
    username = put_data.get("username")
    password = put_data.get("password")

    user = db.session.query(User).filter(User.id == id).first()
    if user is None:
        return jsonify(f"Error: user with id of {id} doesn't exist.")

    if username:
        user.username = username
    if password:
        user.password = password

    db.session.commit()

    return jsonify("User updated successfully")

@app.route("/user/delete/<id>", methods=["DELETE"])
def delete_user(id):
    user = db.session.query(User).filter(User.id == id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify("User deleted successfully")



if __name__ == "__main__":
    app.run(debug=True)