from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'dummy.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
app.app_context().push()


# dummy database

users_books = db.Table('users_books',
                    db.Column('user_id' , db.Integer() , db.ForeignKey('user.id')) ,
                    db.Column('book_id' , db.Integer() , db.ForeignKey('book.id'))
)

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(50) , nullable = False , unique = True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50) , nullable = False)
    books = db.relationship('Book' , secondary = users_books , backref=db.backref('users'))


class Book(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(50) , nullable = False)
    author = db.Column(db.String(50) , nullable = False)
    genre = db.Column(db.String(50) , nullable = False)
    length = db.Column(db.Integer)
    publisher = db.Column(db.String(50) , nullable = False)


@app.route('/')
def index():
    books = Book.query.all()
    return render_template("index.html" , data=books)


@app.route('/login')
def login():
    return render_template("login.html")



@app.route('/register')
def register():
    return render_template("register.html")



if __name__ == '__main__':
    app.run(debug=True)