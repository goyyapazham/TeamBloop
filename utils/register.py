from flask import Flask, render_template, request, session, redirect, url_for
import csv, hashlib, os, sqlite3
from utils import sql

f="data/users.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()

def hash(a):
    return(hashlib.md5(a).hexdigest())

def regi(name, pswrd):
    c = sql.get_all_users()
    for user in c:
		if name == user[0]:
			return "Name Taken!"
    if len(pswrd) < 8:
	    return "Password Too Short, Must Be At Least 8 Characters Long"
    sql.add_user(name, hash(pswrd))
    return "Added"
             

def login(name, pswrd):
    c = sql.get_all_users()
    for user in c:
        if name == user[0]:
            if hash(pswrd) == user[1]:
                return "Welcome"
            return "Incorrect Password"
    return "You need to register"





