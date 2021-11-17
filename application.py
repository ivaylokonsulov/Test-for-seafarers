from cs50 import SQL
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from bs4 import BeautifulSoup as bs
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from functools import wraps
from datetime import datetime
import requests
import csv
import random

# TEST parsing data TEST USPESHEN
#vupros = db.execute("SELECT question, a, b, c, d FROM test1 WHERE id=5")

#print(vupros[0]["question"])

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Opening database
#db = SQL("sqlite:///tests.db")

# ==================================================================== TEST ==========================================================================
con = sqlite3.connect('tests.db', check_same_thread=False)
db = con.cursor()


# ==================================================================== TEST ==========================================================================
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return render_template("apology.html", message="Please, provide an username")
        password = request.form.get("password")
        if not password:
            return render_template("apology.html", message="Please, provide a password")
        confirmation = request.form.get("confirmation")
        if not confirmation or password != confirmation:
            return render_template("apology.html", message="Passwords do not match")

        # If username already exists
        check = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if check:
            return render_template("apology.html", message="Username already exists!")

        hash_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password)


        return index()

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", message="Please, provide a username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", message="Please, provide a password.")


        username = request.form.get("username")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        # TEST =====================================================================================================================
        #return render_template("apology.html", message=rows[0][2])

        # Ensure username exists and password is correct
        if not rows[0][1] or not check_password_hash(rows[0][2], request.form.get("password")):
            return render_template("apology.html", message="Invalid username and/or password")

        # Remember which user has logged in
        # Realno rows predstavlqva tochno edinstveniq red, koito ni e vurnal SQL, AKO imame suvpadenie
        # S detailite (credentials), koito sa bili vuvedeni ot potrebitelq
        # S rows[0]["id"] vzemame informaciqta ot purviq red [0] ot kletka nomer id
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/zavurshi", methods=["POST"])
@login_required
def zavurshi():

    user_id = session["user_id"]

    verni = request.form.get("broi_verni")
    greshni = request.form.get("broi_greshni")
    funkciq = request.form.get("funkciq")
    uspevaemost = request.form.get("uspevaemost")

    # Inserting information about the test into database
    db.execute("INSERT INTO history (id, test, broi_verni, broi_greshni, data, uspevamost) VALUES (?, ?, ?, ?, ?, ?)",
                user_id, funkciq, verni, greshni, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), uspevaemost)
    con.commit()
    return redirect("/")

@app.route("/")
@login_required
def index():

    # Selecting the user who is logged in
    user_id = session["user_id"]
    info = db.execute("SELECT test, broi_verni, broi_greshni, data, uspevamost FROM history WHERE id=?", (user_id,)).fetchall()

    return render_template("index.html", info = info)

@app.route("/test1")
@login_required
def test1():
    # Finding the maximum id contained in the database
    maxa = db.execute("SELECT id FROM test1 ORDER BY id DESC LIMIT 0, 1").fetchall()

    # Defining variables
    i = 0
    random_chisla = list()

    while i < 60:

        chislo = random.randint(1,maxa[0][0])

        # If it is not a duplicate
        if chislo not in random_chisla:
            random_chisla.append(chislo)

        # If it is a duplicate
        else:
            i -= 1

        # Increase i in order to conitnue up to 60 questions
        i += 1

    # Generating empty lists
    test = [{} for _ in range(60)]
    answers = [{} for _ in range(60)]
    otgovori = list()

    # Setting i to 0
    i = 0

    # Iterating and storing questions
    while i < 60:
        test[i] = db.execute("SELECT question, correct FROM test1 WHERE id = ?", (random_chisla[i],)).fetchall()
        answers[i] = db.execute("SELECT a, b, c, d FROM test1 WHERE id = 1").fetchall()
        otgovor = db.execute("SELECT a, b, c, d FROM test1 WHERE id = ?", (random_chisla[i],)).fetchall()
        otgovori = [otgovor[0][0], otgovor[0][1], otgovor[0][2], otgovor[0][3]]
        random.shuffle(otgovori)
        answers[i] = list(otgovori)

        # Increase in order to continue up to 60
        i += 1

    data_all = zip(test,answers)

    return render_template("test1.html", funkciq = "Функция 1", data = data_all)

@app.route("/test2")
@login_required
def test2():
    # Finding the maximum id contained in the database
    maxa = db.execute("SELECT id FROM test2 ORDER BY id DESC LIMIT 0, 1").fetchall()

    # Defining variables
    i = 0
    random_chisla = list()

    while i < 60:

        chislo = random.randint(1,maxa[0][0])

        # If it is not a duplicate
        if chislo not in random_chisla:
            random_chisla.append(chislo)

        # If it is a duplicate
        else:
            i -= 1

        # Increase i in order to conitnue up to 60 questions
        i += 1

    # Generating empty lists
    test = [{} for _ in range(60)]
    answers = [{} for _ in range(60)]
    otgovori = list()

    # Setting i to 0
    i = 0

    # Iterating and storing questions
    while i < 60:
        test[i] = db.execute("SELECT question, correct FROM test2 WHERE id = ?", (random_chisla[i],)).fetchall()
        answers[i] = db.execute("SELECT a, b, c, d FROM test2 WHERE id = 1").fetchall()
        otgovor = db.execute("SELECT a, b, c, d FROM test2 WHERE id = ?", (random_chisla[i],)).fetchall()
        otgovori = [otgovor[0][0], otgovor[0][1], otgovor[0][2], otgovor[0][3]]
        random.shuffle(otgovori)
        answers[i] = list(otgovori)

        # Increase in order to continue up to 60
        i += 1

    data_all = zip(test,answers)

    return render_template("test1.html", funkciq = "Функция 2", data = data_all)

@app.route("/test3")
@login_required
def test3():
    # Finding the maximum id contained in the database
    maxa = db.execute("SELECT id FROM test3 ORDER BY id DESC LIMIT 0, 1").fetchall()

    # Defining variables
    i = 0
    random_chisla = list()

    while i < 60:

        chislo = random.randint(1,maxa[0][0])

        # If it is not a duplicate
        if chislo not in random_chisla:
            random_chisla.append(chislo)

        # If it is a duplicate
        else:
            i -= 1

        # Increase i in order to conitnue up to 60 questions
        i += 1

    # Generating empty lists
    test = [{} for _ in range(60)]
    answers = [{} for _ in range(60)]
    otgovori = list()

    # Setting i to 0
    i = 0

    # Iterating and storing questions
    while i < 60:
        test[i] = db.execute("SELECT question, correct FROM test3 WHERE id = ?", (random_chisla[i],)).fetchall()
        answers[i] = db.execute("SELECT a, b, c, d FROM test3 WHERE id = 1").fetchall()
        otgovor = db.execute("SELECT a, b, c, d FROM test3 WHERE id = ?", (random_chisla[i],)).fetchall()
        otgovori = [otgovor[0][0], otgovor[0][1], otgovor[0][2], otgovor[0][3]]
        random.shuffle(otgovori)
        answers[i] = list(otgovori)

        # Increase in order to continue up to 60
        i += 1

    data_all = zip(test,answers)

    return render_template("test1.html", funkciq = "Функция 3", data = data_all)

@app.route("/test1_full")
@login_required
def test1_full():
    # Finding the maximum id contained in the database
    maxa = db.execute("SELECT id FROM test1 ORDER BY id DESC LIMIT 0, 1").fetchall()

    # Defining variables
    i = 0
    random_chisla = list()

    while i < maxa[0][0]:

        chislo = random.randint(1,maxa[0][0])

        # If it is not a duplicate
        if chislo not in random_chisla:
            random_chisla.append(chislo)

        # If it is a duplicate
        else:
            i -= 1

        # Increase i in order to conitnue up to 60 questions
        i += 1

    # Generating empty lists
    test = [{} for _ in range(maxa[0][0])]
    answers = [{} for _ in range(maxa[0][0])]
    otgovori = list()

    # Setting i to 0
    i = 0

    # Iterating and storing questions
    while i < maxa[0][0]:
        test[i] = db.execute("SELECT question, correct FROM test1 WHERE id = ?", (random_chisla[i],)).fetchall()
        answers[i] = db.execute("SELECT a, b, c, d FROM test1 WHERE id = 1").fetchall()
        otgovor = db.execute("SELECT a, b, c, d FROM test1 WHERE id = ?", (random_chisla[i],)).fetchall()
        otgovori = [otgovor[0][0], otgovor[0][1], otgovor[0][2], otgovor[0][3]]
        random.shuffle(otgovori)
        answers[i] = list(otgovori)

        # Increase in order to continue up to max
        i += 1

    data_all = zip(test,answers)


    return render_template("test1.html", funkciq = "Функция 1 - всички въпроси", data = data_all)


@app.route("/test2_full")
@login_required
def test2_full():
    # Finding the maximum id contained in the database
    maxa = db.execute("SELECT id FROM test2 ORDER BY id DESC LIMIT 0, 1").fetchall()

    # Defining variables
    i = 0
    random_chisla = list()

    while i < maxa[0][0]:

        chislo = random.randint(1,maxa[0][0])

        # If it is not a duplicate
        if chislo not in random_chisla:
            random_chisla.append(chislo)

        # If it is a duplicate
        else:
            i -= 1

        # Increase i in order to conitnue up to 60 questions
        i += 1

    # Generating empty lists
    test = [{} for _ in range(maxa[0][0])]
    answers = [{} for _ in range(maxa[0][0])]
    otgovori = list()

    # Setting i to 0
    i = 0

    # Iterating and storing questions
    while i < maxa[0][0]:
        test[i] = db.execute("SELECT question, correct FROM test2 WHERE id = ?", (random_chisla[i],)).fetchall()
        answers[i] = db.execute("SELECT a, b, c, d FROM test2 WHERE id = 1").fetchall()
        otgovor = db.execute("SELECT a, b, c, d FROM test2 WHERE id = ?", (random_chisla[i],)).fetchall()
        otgovori = [otgovor[0][0], otgovor[0][1], otgovor[0][2], otgovor[0][3]]
        random.shuffle(otgovori)
        answers[i] = list(otgovori)

        # Increase in order to continue up to max
        i += 1

    data_all = zip(test,answers)


    return render_template("test1.html", funkciq = "Функция 2 - всички въпроси", data = data_all)

@app.route("/test3_full")
@login_required
def test3_full():
    # Finding the maximum id contained in the database
    maxa = db.execute("SELECT id FROM test3 ORDER BY id DESC LIMIT 0, 1").fetchall()

    # Defining variables
    i = 0
    random_chisla = list()

    while i < maxa[0][0]:

        chislo = random.randint(1,maxa[0][0])

        # If it is not a duplicate
        if chislo not in random_chisla:
            random_chisla.append(chislo)

        # If it is a duplicate
        else:
            i -= 1

        # Increase i in order to conitnue up to 60 questions
        i += 1

    # Generating empty lists
    test = [{} for _ in range(maxa[0][0])]
    answers = [{} for _ in range(maxa[0][0])]
    otgovori = list()

    # Setting i to 0
    i = 0

    # Iterating and storing questions
    while i < maxa[0][0]:
        test[i] = db.execute("SELECT question, correct FROM test3 WHERE id = ?", (random_chisla[i],)).fetchall()
        answers[i] = db.execute("SELECT a, b, c, d FROM test3 WHERE id = 1").fetchall()
        otgovor = db.execute("SELECT a, b, c, d FROM test3 WHERE id = ?", (random_chisla[i],)).fetchall()
        otgovori = [otgovor[0][0], otgovor[0][1], otgovor[0][2], otgovor[0][3]]
        random.shuffle(otgovori)
        answers[i] = list(otgovori)

        # Increase in order to continue up to max
        i += 1

    data_all = zip(test,answers)


    return render_template("test1.html",funkciq = "Функция 3 - всички въпроси", data = data_all)



        #random_vupros = db.execute("SELECT * FROM test1 WHERE id=?", chislo)

#print(chislo)


#print(random_vupros[0]["question"], random_vupros[0]["a"], random_vupros[0]["b"], random_vupros[0]["c"], random_vupros[0]["d"])

# TESTVANE DALI DVETE STOINOSTI ZA PRAVILEN OTGOVOR SUVPADAT. TEST USPESHEN

#question = db.execute("SELECT question,a,b,c,d FROM test1 WHERE id=1")
#correct = db.execute("SELECT correct FROM test1 WHERE id=1")

#if question[0]["d"] == correct[0]["correct"]:
    #print("Correct")
#else:
    #print(correct[0]["correct"])
    #print(question[0]["d"])