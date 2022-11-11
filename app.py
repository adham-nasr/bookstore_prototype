from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# dummy database

book1 = {"name":"A" , "length":5}
book2 = {"name":"b" , "length":4}
book3 = {"name":"c" , "length":3}


data = [book1,book2,book3]






@app.route('/')
def index():
    return render_template("index.html" , data=data)


@app.route('/login')
def login():
    return render_template("login.html")



@app.route('/register')
def register():
    return render_template("register.html")



if __name__ == '__main__':
    app.run(debug=True)