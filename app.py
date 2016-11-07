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
	d = {}
	userid = sql.get_userid(session["user"])
	ids = sql.get_stories(userid, viewing_on=True)
	for id in ids:
		author = sql.query('SELECT username FROM users WHERE id = ' + str(sql.get_author(id)))
		d[id] = [sql.get_title(id),author]
	return render_template("main.html", user = session["user"], dict = d)

@app.route("/newstory/", methods = ['GET'])
def newstory():
     return render_template("newstory.html")
   
@app.route("/addnewstory/", methods = ['POST'])
def addnewstory():
	userid = sql.get_userid(session["user"])
	sql.add_story(request.form['title'], userid, request.form['story'])
	return redirect(url_for('welcome'))

@app.route("/updated/", methods = ['POST'])
def updated():
       userid = sql.get_userid(session["user"])
       sql.add_update(userid, request.form["storyID"], request.form["story"])
       return redirect(url_for('welcome'))
	   
@app.route("/update/", methods = ['GET'])
def update():
	return render_template("updatestory.html")

@app.route("/viewupdateable/", methods = ['GET'])
def viewupdateable():
	d = {}
	
	return render_template("viewupdateable.html", dict = d)

@app.route("/viewstory/<storyid>", methods = ['GET'])	  
def viewstory(storyid):
	storystring = ""
	updateL = sql.get_all_updates(storyid)
	for u in updateL:
		print sql.get_update(u)
		print sql.get_update(u)[0]
		storystring += sql.get_update(u)[0]
	return render_template("viewstory.html", title = sql.get_title(storyid), story = storystring)
       
@app.route("/bye/", methods = ['POST'])
def bye():
     if "user" in session:
          session.pop("user")
     return redirect(url_for('main'))

  
if __name__ =="__main__":
     app.debug=True
     app.run()



