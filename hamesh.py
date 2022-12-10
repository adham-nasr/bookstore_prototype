from manage import db,User,Book

print(User.query.filter_by(username="a",password="a").all())

print(Book.query.all()[:10])