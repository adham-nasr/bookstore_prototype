import csv

from manage import db,Book

filename = "books.csv"

rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        book = Book(title = row['Title'] , author=row['Author'] , genre=row['Genre'] , length = row['Height'] , publisher=row['Publisher'])
        db.session.add(book)
    
    db.session.commit()


