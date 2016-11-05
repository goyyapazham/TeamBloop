from flask import Flask, render_template, request, session, redirect, url_for
import csv, hashlib, os, sqlite3
from utils import sql

f="data/users.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()

def hesh(a):
    return(hashlib.md5(a).hexdigest())

def regi(a, b):
    c = csv.reader(open("data/name.csv"))
    for d in c:
        if a == d[0]:
            return "Name Taken!"
	if len(b) < 8:
	    return "Password Too Short, Must Be At Least 8 Characters Long"
    with open('data/name.csv', 'a') as e:
        f = csv.writer(e)
        f.writerow([a, hesh(b)])
    return "Added"
             

def login(a, b):
    c = csv.reader(open("data/name.csv"))
    for d in c:
        if a == d[0]:
            if hesh(b)==d[1]:
                return "Welcome"
            return "Incorrect Password"
    return "You need to register"





