import sqlite3 as sql
import csv


def init(db):
    cur = db.cursor()
    cur.execute('CREATE TABLE users (id INTEGER, username TEXT, password TEXT)')
    cur.execute('CREATE TABLE stories (id INTEGER, title TEXT, latestid INTEGER)')
    cur.execute('CREATE TABLE updates (id INTEGER, userid INTEGER, storyid INTEGER, content TEXT)')
    db.commit()


def get_stories(db, userid, viewing_on):
    cur = db.cursor()
    req = cur.execute('SELECT stories.id FROM stories, updates WHERE ')


def get_all_updates
