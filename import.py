import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    cols = next(reader)
    # print(cols)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) \
			VALUES (:isbn, :title, :author, :year)", {
            "isbn": isbn,
            "title": title,
            "author": author,
            "year": year
        })
        print("added book({}, {}, {}, {}".format(isbn, title, author, year))
    db.commit()

    # books = db.execute("SELECT * FROM books")
    # for book in books:
    #     print(book)
    # db.commit()
if __name__ == "__main__":
    main()
