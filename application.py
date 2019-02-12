import os
import hasher
from flask import Flask, session, render_template, redirect, json, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

bookTitles = ["Krondor: The Betrayal", "The Dark Is Rising", "The Black Unicorn", "I, Robot", "Four Blondes", "Love, Stargirl", "The Tenth Circle", "Vanishing Acts", "Aztec", "Marlfox", "Lady Midnight", "The Secret Keeper"]

@app.route("/")
def index():
    return render_template("index.html", books=bookTitles)

@app.route("/contact")
def contact():
	return render_template("contact.html")
	
@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/book")
def book():
	return render_template("bookInfo.html")
	
@app.route("/user")
def user():
	return render_template("userInfo.html")


@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/sign_up")
def sign_up():
	return render_template("sign_up.html")