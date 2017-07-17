from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
app = Flask(__name__)
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
app.jinja_env.filters["usd"] = usd
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///finance.db")
@app.route("/")
@login_required
def index():
    portfolio_symbols = db.execute("SELECT shares_amt, symbol \
                                    FROM portfolio WHERE id = :id", \
                                    id=session["user_id"])
    
    Cash_in_total = 0
    
    
    for portfolio_symbol in portfolio_symbols:
        symbol = portfolio_symbol["symbol"]
        shares_amt = portfolio_symbol["shares"]
        stock_amt = lookup(symbol)
        total_amt = shares * stock["price"]
        Cash_in_total  += total_amt
        db.execute("UPDATE portfolio SET price=:price, \
                    total_amt=:total_amt WHERE id=:id AND symbol=:symbol", \
                    price=usd(stock["price"]), \
                    total_amt=usd(total_amt), id=session["user_id"], symbol=symbol)
    updated_cash_amt = db.execute("SELECT cash FROM users \
                               WHERE id=:id", id=session["user_id"])
    Cash_in_total  += updated_cash_amt[0]["cash"]
    updated_portfolio = db.execute("SELECT * from portfolio \
                                    WHERE id=:id", id=session["user_id"])
                                    
    return render_template("index.html", stocks=updated_portfolio, \
                            cash=usd(updated_cash_amt[0]["cash"]), total_amt= usd(Cash_in_total) )

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    if request.method == "GET":
        return render_template("buy.html")
    else:
        # ensure proper symbol
        stock_amt = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol")
        
        # ensure proper number of shares
        try:
            shares_amt = int(request.form.get("shares"))
            if shares_amt < 0:
                return apology("Shares should be a positive integer value")
        except:
            return apology("Shares should be a positive integer value")
        user_money= db.execute("SELECT cash FROM users WHERE id = :id", \
                            id=session["user_id"])
        if not  user_money or float( user_money[0]["cash"]) < stock_amt["price"] * shares_amt:
            return apology("Not enough money in user account")
        db.execute("INSERT INTO histories (symbol, shares_amt, price, id) \
                    VALUES(:symbol, :shares_amt, :price, :id)", \
                    symbol=stock_amt["symbol"], shares_amt=shares_amt, \
                    price=usd(stock_amt["price"]), id=session["user_id"])
                       
                     
        db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=stock_amt["price"] * float(shares_amt))
                        
        
        user_shares_amt = db.execute("SELECT shares_amt FROM portfolio \
                           WHERE id = :id AND symbol=:symbol", \
                           id=session["user_id"], symbol=stock_amt["symbol"])
                           
       
        if not user_shares_amt:
            db.execute("INSERT INTO portfolio (name, shares_amt, price, total_amt, symbol, id) \
                        VALUES(:name, :shares_amt, :price, :total_amt, :symbol, :id)", \
                        name=stock_amt["name"], shares_amt=shares_amt, price=usd(stock["price"]), \
                        total_amt=usd(shares_amt * stock_amt["price"]), \
                        symbol=stock_amt["symbol"], id=session["user_id"])
                        
        
        else:
            total_shares = user_shares_amt[0]["shares"] + shares_amt
            db.execute("UPDATE portfolio SET shares_amt=:shares_amt \
                        WHERE id=:id AND symbol=:symbol", \
                        shares_amt=total_shares, id=session["user_id"], \
                        symbol=stock_amt["symbol"])
        
        
        return redirect(url_for("index"))

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    histories = db.execute("SELECT * from histories WHERE id=:id", id=session["user_id"])
    
    return render_template("history.html", histories=histories)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    session.clear()
    if request.method == "POST":

        
        if not request.form.get("username"):
            return apology("must provide valid  username")

       
        elif not request.form.get("password"):
            return apology("must provide correct password")

        
        username_row = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        
        if len(username_row) != 1 or not pwd_context.verify(request.form.get("password"), username_row[0]["hash"]):
            return apology("invalid username and/or password")
        session["user_id"] = username_row[0]["id"]
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    if request.method == "POST":
        username_row = lookup(request.form.get("symbol"))
        
        if not username_row:
            return apology("Invalid Symbol")
            
        return render_template("quoted.html", stock_amt=username_row)
    
    else:
        return render_template("quote.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    if request.method == "POST":
        
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")
            
        # ensure password was submitted    
        elif not request.form.get("password"):
            return apology("Must provide password")
        
        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("passwordagain"):
            return apology("password doesn't match")
        
        # insert the new user into users, storing the hash of the user's password
        result = db.execute("INSERT INTO users (username, hash) \
                             VALUES(:username, :hash)", \
                             username=request.form.get("username"), \
                             hash=pwd_context.encrypt(request.form.get("password")))
                 
        if not result:
            return apology("Username already exist")
            
            # remember which user has logged in
        session["user_id"] = result

        # redirect user to home page
        return redirect(url_for("index"))
    
    else:
        return render_template("register.html")  
    

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        # ensure proper symbol
        stock_amt = lookup(request.form.get("symbol"))
        if not stock_amt:
            return apology("Invalid Symbol")
        
        # ensure proper number of shares
        try:
            shares_amt = int(request.form.get("shares"))
            if shares_amt< 0:
                return apology("Shares should be positive a integer value")
        except:
            return apology("Shares should be positive a integer value")
        user_shares_amt = db.execute("SELECT shares_amt FROM portfolio \
                                 WHERE id = :id AND symbol=:symbol", \
                                 id=session["user_id"], symbol=stock["symbol"])
        if not user_shares_amt or int(user_shares_amt[0]["shares"]) < shares_amt:
            return apology("Not enough shares in user's account")
         
        db.execute("INSERT INTO histories (symbol, shares_amt, price, id) \
                    VALUES(:symbol, :shares_amt, :price, :id)", \
                    symbol=stock_amt["symbol"], shares_amt=-shares_amt, \
                    price=usd(stock_amt["price"]), id=session["user_id"])
                       
        # update user cash (increase)              
        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id", \
                    id=session["user_id"], \
                    purchase=stock_amt["price"] * float(shares_amt))
                        
        # decrement the shares count
        total_shares = user_shares_amt[0]["shares"] - shares_amt
        
        # if after decrement is zero, delete shares from portfolio
        if total_shares == 0:
            db.execute("DELETE FROM portfolio \
                        WHERE id=:id AND symbol=:symbol", \
                        id=session["user_id"], \
                        symbol=stock_amt["symbol"])
        # otherwise, update portfolio shares count
        else:
            db.execute("UPDATE portfolio SET shares_amt=:shares_amt \
                    WHERE id=:id AND symbol=:symbol", \
                    shares_amt=stotal_shares, id=session["user_id"], \
                    symbol=stock_amt["symbol"])
        
        # return to index
        return redirect(url_for("index"))


