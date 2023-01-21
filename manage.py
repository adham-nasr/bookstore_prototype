from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'dummy.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='SUPERSECRETKEY'

db = SQLAlchemy(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#db.create_all()


# dummy database

users_books = db.Table('users_books',
                    db.Column('user_id' , db.Integer() , db.ForeignKey('user.id')) ,
                    db.Column('book_id' , db.Integer() , db.ForeignKey('book.id'))
)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(50) , nullable = False , unique = True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50) , nullable = False)
    books = db.relationship('Book' , secondary = users_books , backref=db.backref('users'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Book(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(50) , nullable = False)
    author = db.Column(db.String(50) , nullable = False)
    genre = db.Column(db.String(50) , nullable = False)
    length = db.Column(db.Integer)
    publisher = db.Column(db.String(50) , nullable = False)


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField(validators=[InputRequired(),Length(min=1,max=30)])
    password = PasswordField(validators=[InputRequired(),Length(min=1,max=40)])
    password2 = PasswordField(validators=[InputRequired(),Length(min=1,max=40)])
    email = StringField(validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])


class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField(validators=[InputRequired(),Length(min=1,max=30)])
    password = PasswordField(validators=[InputRequired(),Length(min=1,max=40)])

@app.route('/')
def index():
    books = Book.query.all()
    #print(books)
    a = db.session.query(Book).group_by(Book.genre).all()
 #   print(a)
    genres=[]
    for book in a:
        genres.append(book.genre)
    genre_book = []
    for genre in genres:
        obj={"name":genre,"books1":Book.query.filter_by(genre=genre).limit(5).all()}
        books2=Book.query.filter_by(genre=genre).all()[5:]
        sub_books=[]
        l=[]
        i=0
        for book in books2:
            l.append(book)
            i=i+1
            if i==5:
                sub_books.append(l)
                l=[]
                i=0
        if len(l):
            sub_books.append(l)
        obj["books2"]=sub_books
        genre_book.append(obj)
    print(genre_book[0])
    return render_template("index.html" , data=genre_book)


@app.route('/login' , methods=["GET","POST"])
def login():
    if request.method == "GET":
        print(db.session.query(Book).all())
        return render_template("login.html")
    
    username = request.form["username"]
    password = request.form["password"]
    #phonenumber = request.form["phonenumber"]

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username,password=password).first()
        print(user)
        if user:
            print("loggged in")
            login_user(user)
            return redirect("/books/get")
        return render_template("error.html",error="Invalid username or password")
    else:
        return render_template("login.html",form=form) 



@app.route('/register' , methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    #phonenumber = request.form["phonenumber"]

    form = RegisterForm()
    if form.validate_on_submit():
        if len(User.query.filter_by(username=username).all()) == 0 and len(User.query.filter_by(email=email).all())==0:
            user = User(username=username,email=email,password=password)
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
        return render_template("error.html",error="User already exists")
    else:
        return render_template("register.html",form=form) 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
    

@app.route('/books/add',methods=["GET","POST"])
@login_required 
def addbooks():
    if request.method == "GET":
        books = Book.query.all()[:15]
        return render_template("add.html" , books=books)
    book_id = request.form["book"]
    book = Book.query.filter_by(id=book_id)[0]
    print(book)
    user = current_user
    user.books.append(book)
    db.session.commit()
    return redirect('/books/get')


@app.route('/books/get')
@login_required
def getbooks():
    user = current_user
    books = user.books
    print(books)
    return render_template("mybooks.html" , books=books)



    user = User(username=name,email=email,password=password)
    db.session.add(user)
    db.session.commit()

    return render_template("mybooks.html")



if __name__ == '__main__':
    app.run(debug=True)