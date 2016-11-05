from flask import Flask, render_template, request, session, redirect, url_for
from utils import register, sql
import os, sqlite3

f="data/users.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()

app = Flask(__name__)

app.secret_key = os.urandom(32)
@app.route("/")
def main():
     if "user" in session:
         return redirect(url_for('welcome'))
     return render_template("login.html")

@app.route("/authenticate/", methods = ['POST'])
def auth():
        s = register.login(request.form["user"],request.form["password"])
        if s == "Welcome":
            session["user"] = request.form["user"]
            return redirect(url_for('welcome'))
        return render_template("login.html", message = s)

@app.route("/reg/", methods = ['POST'])
def reg():
        s = register.regi(request.form["user"],request.form["password"])
        if s == "Added":
            session["user"] = request.form["user"]
            return redirect(url_for('welcome'))
        return render_template("login.html", message = s)
                         
@app.route("/welcome/", methods = ['GET'])
def welcome():
     return render_template("main.html", user = session["user"], dict = {"Story":"Bob"})
	 
@app.route("/newstory/", methods = ['GET'])
def newstory():
	return render_template("newstory.html")
	
@app.route("/addnewstory/", methods = ['POST'])
def addnewstory():
	#sql.add_story("users.db", request.form['title'], userid, init_update):
	return redirect(url_for('welcome'))
	
@app.route("/bye/", methods = ['POST'])
def bye():
     if "user" in session:
        session.pop("user")
     return redirect(url_for('main'))

  
if __name__ =="__main__":
    app.debug=True
    app.run()



