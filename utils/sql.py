import sqlite3 as sql
import csv


def init(db):
    cur = db.cursor()
    cur.execute(
        'CREATE TABLE users (id INTEGER, username TEXT, password TEXT)')
    cur.execute(
        'CREATE TABLE stories (id INTEGER, title TEXT, latestid INTEGER)')
    cur.execute('''CREATE TABLE updates
        (id INTEGER, userid INTEGER, storyid INTEGER, content TEXT)''')
    db.commit()


def get_stories(db, userid, viewing_on):
    cur = db.cursor()
    q = '''SELECT updates.storyid FROM updates WHERE
    updates.userid = ''' + str(userid)
    res = cur.execute(q)
    return [i[0] for i in res]


def add_story(db, title, userid, init_update):
    cur = db.cursor()
    res = cur.execute('SELECT id FROM stories')
    newid = max([i[0] for i in res]) + 1
    cur.execute('''INSERT INTO updates VALUES
    (0, ''' + str(userid) + ', ' + str(newid) + ', ' + init_update + ')')
    cur.execute(
        'INSERT INTO stories VALUES (' + str(newid) + ', ' + title + ', 0)')
    db.commit()


def get_title(db, storyid):
    return db.cursor().execute(
        'SELECT title FROM stories WHERE id = ' + str(storyid))[0][0]
