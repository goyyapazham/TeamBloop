import sqlite3 as sql
import csv


def init(db):
    cur = db.cursor()
    cur.execute(
        'CREATE TABLE users (id INTEGER, username TEXT, password TEXT)')
    cur.execute(
        'CREATE TABLE stories (id INTEGER, title TEXT, latestid INTEGER)')
    cur.execute('''CREATE TABLE updates
        (id INTEGER, userid INTEGER, storyid INTEGER)''')
    cur.execute('''INSERT INTO stories VALUES (-1, "", -1)''')
    db.commit()


def get_stories(db, userid, viewing_on=True):  # XXX viewing_on not implemented
    cur = db.cursor()
    if viewing_on:
        q = '''SELECT updates.storyid FROM updates WHERE
        updates.userid = ''' + str(userid)
    res = cur.execute(q)
    return [i[0] for i in res]


def add_story(db, title, userid, init_update):
    cur = db.cursor()
    res = cur.execute('SELECT id FROM stories')
    newid = max([i[0] for i in res]) + 1
    cur.execute('INSERT INTO updates VALUES (0, '
        + str(userid) + ', ' + str(newid) + ', "' + init_update + '")')
    cur.execute(
        'INSERT INTO stories VALUES (' + str(newid) + ', "' + title + '", 0)')
    db.commit()


def get_title(db, storyid):
    title_holder = db.cursor().execute(
        'SELECT title FROM stories WHERE id = ' + str(storyid))
    for i in title_holder:
        return i[0]


def is_edited(db, storyid, userid):
    return storyid in get_stories(db, userid)


def get_latest_update(db, storyid):
    c_h = db.cursor().execute(
        'SELECT latestid FROM stories WHERE id = %d'%(storyid))
    for i in c_h:
        return i[0]


def get_all_updates(db, storyid):
    return [i[0] for i in db.cursor().execute(
        'SELECT id FROM updates WHERE storyid = %d'%(storyid))]


def get_update(updateid):  # ONLY function that doesn't use database, takes uid and accesses file
    with open(str(updateid) + '.txt') as f:
        return f.read()

def next_updateid(db):
    uids = [i[0] for i in db.cursor().execute(
        'SELECT id FROM updates')]
    return max(uids) + 1


def next_storyid(db):
    sids = [i[0] for i in db.cursor().execute(
        'SELECT id FROM stories')]
    return max(sids) + 1


def next_userid(db):
    uids = [i[0] for i in db.cursor().execute(
        'SELECT id FROM users')]
    return max(uids) + 1


if __name__ == '__main__':  #tests
    db = sql.connect('b.db')  # test database
    # execute with python -i utils/sql.py, then test functions in interpreter
