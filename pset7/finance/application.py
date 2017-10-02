from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

import time

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

    #look up stocks for user
    entries = db.execute("SELECT *, SUM(shares) FROM portfolio WHERE id = '{}' GROUP BY symbol".format(session["user_id"]))
    user = db.execute("SELECT * FROM users WHERE id = '{}'".format(session["user_id"]))
    stocks = []
    total_value = user[0]["cash"]

    for entry in entries:
        stock = {
            "symbol": "",
            "name": "",
            "shares": 0,
            "price": 0,
            "value": 0
        }

        current = lookup(entry["symbol"])

        stock["symbol"] = entry["symbol"]
        stock["price"] = current["price"]
        stock["name"] = current["name"]
        stock["shares"] = entry["SUM(shares)"]
        stock["value"] = current["price"] * entry["SUM(shares)"]
        total_value += stock["value"]
        stocks.append(stock)

    return render_template("index.html", user=user[0], stocks=stocks, total_value = total_value)
    #sum up stocks for each company

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

        #Look up the stock for given symbol
        quote = lookup(request.form.get("symbol"))

        #If there is no stock for that symbol
        if not quote:
            return apology("must provide a real stock symbol")

        #If they aren't buying a positive amount of stocks
        if int(request.form.get("number")) < 1:
            return apology("Please enter an integer greater than 0")

        #Get how much money user has and how much they will need
        user_money = db.execute("SELECT cash FROM users WHERE id = '{}'".format(session["user_id"]))
        req_money = quote["price"] * int(request.form.get("number"))

        #If user doesn't have enough money
        if user_money[0]["cash"] < req_money:
            return apology("You do not have enough funds")

        db.execute("INSERT INTO 'portfolio' (id, symbol, shares, price, time) VALUES ('{}', '{}', '{}', '{}', '{}')".format(session["user_id"], request.form.get("symbol"), int(request.form.get("number")), int(quote["price"]), time.asctime( time.localtime(time.time()) )))

        #Update their money
        db.execute("UPDATE 'users' SET cash = '{}' WHERE id = '{}'".format(user_money[0]["cash"]-req_money, session["user_id"]))

        #Redirect back to index
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

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
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide username")

        #Look up the stock for given symbol
        quote = lookup(request.form.get("symbol"))

        #If there is no stock for that symbol
        if not quote:
            return apology("must provide a real stock symbol")

        #If they aren't selling a positive amount of stocks
        if int(request.form.get("number")) < 1:
            return apology("Please enter an integer greater than 0")

        #Get how many stocks the user has
        user_stock = db.execute("SELECT *, SUM(shares) FROM portfolio WHERE id = '{}' AND symbol = '{}'".format(session["user_id"], request.form.get("symbol")))
        user = db.execute("SELECT * FROM users WHERE id = '{}'".format(session["user_id"]))

        if user_stock[0]["SUM(shares)"] < int(request.form.get("number")):
            return apology("You do not have enough stock")

        #Get how much money they will receive
        received_money = quote["price"] * int(request.form.get("number"))


        #Update their money
        db.execute("UPDATE 'users' SET cash = '{}' WHERE id = '{}'".format(user[0]["cash"]+received_money, session["user_id"]))
        db.execute("INSERT INTO 'portfolio' (id, symbol, shares, price, time) VALUES ('{}', '{}', '{}', '{}', '{}')".format(session["user_id"], request.form.get("symbol"), -int(request.form.get("number")), int(quote["price"]), time.asctime( time.localtime(time.time()) )))

        #Redirect back to index
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html")
