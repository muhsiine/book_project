import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def add_user(uname, umail, upass, uicon=None):
    if uicon is None:
        db.execute('INSERT INTO users (uname, upass, umail) VALUES(:uname, :upass, :umail)', {
                   "uname": uname, "upass": upass, "umail": umail})
    else:
        db.execute('INSERT INTO users (uname, upass, umail, uicon) VALUES(:uname, :upass, :umail, :uicon)', {
                   "uname": uname, "upass": upass, "umail": umail, "uicon": uicon})
    db.commit()


def update_user(uid):
    db.execute('UPDATE users SET uname = :uname, upass = :upass, umail = :umail, uicon = :uicon WHERE uid = :uid', {
               "uname": 'newname', "upass": 'newpass', "umail": 'newmail', "uicon": 'newicon'})
    db.commit()


def remove_user(uid):
    db.execute('DELETE FROM users WHERE uid = :uid', {"uid": uid})
    db.commit()


def get_all_users():
    users = db.execute('SELECT uid, uname, umail FROM users;').fetchall()
    return users


def get_user_by_id(uid):
    user = db.execute("SELECT * FROM users WHERE uid = :uid",
                      {"uid": uid}).fetchone()
    return user

def get_user_by(uname, upass):
    user = db.execute("SELECT * FROM users WHERE uname = :uname AND upass = :upass",
                      {"uname": uname, "upass": upass}).fetchone()
    return user

def get_book_by_isbn(isbn):
    book = db.execute('SELECT * FROM books WHERE isbn = :isbn',
                      {"isbn": isbn}).fetchone()
    return book

def get_top_books(limit):
	books = db.execute('SELECT * FROM books LIMIT :lim', {"lim":limit}).fetchall()
	return books


def add_review(uid, isbn, comment, rate):
    db.execute('INSERT INTO reviews (uid, isbn, comment, rate) VALUES(:uid, :isbn, :comment, :rate)', {
               "uid": uid, "isbn": isbn, "comment": comment, "rate": rate})
    db.commit()


def get_review(uid, isbn):
    review = db.execute('SELECT * FROM reviews WHERE uid = :uid AND isbn = :isbn',
                        {"uid": uid, "isbn": isbn}).fetchone()
    return review
    # print(review.comment)


def remove_review(uid, isbn):
    db.execute('DELETE FROM reviews WHERE uid = :uid AND isbn = :isbn', {
               "uid": uid, "isbn": isbn})
    db.commit()


def get_all_reviews(isbn):
    reviews = db.execute(
        'SELECT * FROM reviews WHERE isbn = :isbn', {"isbn": isbn}).fetchall()
    return reviews
    # print(len(reviews))


def remove_book(isbn):
    db.execute('DELETE FROM books WHERE isbn = :isbn', {"isbn": isbn})
    db.commit()


# if __name__ == '__main__':
# 	books = get_top_books(10)
# 	for book in books:
# 		print(book)