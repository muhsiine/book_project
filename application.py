import manage_db as mdb
import hasher
from flask import Flask, session, render_template, redirect, json, url_for, request, flash
from flask_session import Session
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

books = mdb.get_top_books(12)


@app.route("/")
def index():
    return render_template("index.html", books=books)


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


@app.route("/check_login", methods=["POST"])
def check_login():
    if session.get("user") is None:
        uname = request.form['username']
        upass = request.form['userpass']
        upass = hasher.hashpass(upass)
        user = mdb.get_user_by(uname, upass)
        if user is not None:
            session['user'] = user
        else:
            return "User not found" # todo make it return to the sign in page and mention the error 
    return redirect(url_for('index'))


@app.route("/check_signup", methods=["POST"])
def check_signup():
    # print(request.files)
    uname = request.form['username']
    umail = request.form['mail']
    upass = request.form['password']
    upass = hasher.hashpass(upass)

    if 'file' not in request.files:
        mdb.add_user(uname, umail, upass)
        return redirect(url_for('login'))

    file = request.files['file']
    filename = uname + "_"+file.filename
    print(uname, umail, upass, filename)
    if file.filename == '':
        flash('No file part')
        return "Failed to upload"
    if file and allowed_file(file.filename):
        filename = secure_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mdb.add_user(uname, umail, upass, filename)
    return redirect(url_for('login'))

@app.route("/log_out")
def log_out():
    session.pop('user', None)
    return redirect(url_for('index'))