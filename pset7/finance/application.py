from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

####################################
##      CONFIG STUFF
####################################

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

####################################
##  ROUTES
####################################

############
#   Index
############

@app.route("/")
@login_required
def index():
    return apology("TODO")

############
#   Buy
############

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide username")

        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("must provide a real stock symbol")

        if int(request.form.get("number")) < 1:
            return apology("Please enter an integer greater than 0")


        user_money = db.execute("SELECT cash FROM users WHERE id = '{}'".format(session["user_id"]))
        req_money = int(quote["price"]) * int(request.form.get("number"))


        if user_money[0]["cash"] < req_money:
            return apology("You do not have enough funds")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

    return apology("TODO")

############
#   History
############

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return apology("TODO")

############
#   Login
############

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

############
#   Logout
############

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


############
#   Quote
############

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")

        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("must provide a real stock symbol")

        # redirect user to home page
        return render_template("quoted.html", quote=quote)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

############
#   Register
############

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        elif request.form.get("password") != request.form.get("password_conf"):
            return apology("passwords must match")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) >= 1:
            return apology("username already exists")

        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


############
#   Sell
############

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    return apology("TODO")
