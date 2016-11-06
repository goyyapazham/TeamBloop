import sqlite3
import csv

f="data/users.db"

def init():
    db = sqlite3.connect(f)
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, password TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS stories (id INTEGER, title TEXT, latestid INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS updates (id INTEGER, userid INTEGER, storyid INTEGER, content TEXT)")
    cur.execute("INSERT INTO stories VALUES (-1, '', -1)")
    cur.execute("INSERT INTO updates VALUES (-1, -1, -1, '')")
    cur.execute("INSERT INTO users VALUES (-1, '', '')")
    # need base, unused data to do next id functions
    db.commit()
    db.close()
    

def add_user(user, password):
    db = sqlite3.connect(f)
    cur = db.cursor()
    q = "INSERT INTO users VALUES (%d, \'%s\', \'%s\')"%(next_userid(db), user, password)
    print q
    cur.execute(q)
    db.commit()
    db.close()


def get_stories(userid, viewing_on=True):  # XXX viewing_on not implemented
    db = sqlite3.connect(f)
    cur = db.cursor()
    if viewing_on:
        q = '''SELECT updates.storyid FROM updates WHERE
        updates.userid = ''' + str(userid)
    res = cur.execute(q)
    db.close()
    return [i[0] for i in res]


def add_story(title, userid, init_update):
    db = sqlite3.connect(f)
    cur = db.cursor()
    newid = next_storyid(db)
    newupid = next_updateid(db)
    cur.execute(
        'INSERT INTO stories VALUES (' + str(newid)
        + ', "' + title + '",' + str(newupid) + ')')
    db.commit()
    add_update(db, userid, newid, init_update)
    db.close()


def add_update(userid, storyid, content):
    db = sqlite3.connect(f)
    cur = db.cursor()
    upid = next_updateid(db)
    cur.execute("INSERT INTO updates VALUES (%d, %d, %d, \'%s\')"%(upid, userid, storyid, content))
    db.commit()
    db.close()


def get_title(storyid):
    db = sqlite3.connect(f)
    title_holder = db.cursor().execute(
        'SELECT title FROM stories WHERE id = ' + str(storyid))
    db = sqlite3.connect(f)
    for i in title_holder:
        return i[0]


def get_all_users():
    db = sqlite3.connect(f)
    cur = db.cursor()
    res = cur.execute("SELECT * FROM users")
    L = []
    for row in res:
        L += [[row[1],row[2]]]
    db.commit()
    db.close()
    return L

#I don't understand how you've implemented this function - what is it supposed
#to do?
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


run_init = False
db = sqlite3.connect(f)
cur = db.cursor()
res = cur.execute("SELECT id FROM users")
try:
    if res[0] != -1:
        run_init = True
except:
    if run_init:
        init()
db.commit()
db.close()
