import sqlite3
import csv

f="data/users.db"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()

def init(db):
    cur = db.cursor()
    cur.execute(
        'CREATE TABLE users (id INTEGER, username TEXT, password TEXT)')
    cur.execute(
        'CREATE TABLE stories (id INTEGER, title TEXT, latestid INTEGER)')
    cur.execute('''CREATE TABLE updates
        (id INTEGER, userid INTEGER, storyid INTEGER)''')
    cur.execute('''INSERT INTO stories VALUES (-1, "", -1)''')
    cur.execute('''INSERT INTO updates VALUES (-1, -1, -1)''')
    cur.execute('''INSERT INTO users VALUES (-1, "", "")''')
    # need base, unused data to do next id functions
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
    newid = next_storyid(db)
    newupid = next_updateid(db)
    cur.execute(
        'INSERT INTO stories VALUES (' + str(newid)
        + ', "' + title + '",' + str(newupid) + ')')
    db.commit()
    add_update(db, userid, newid, init_update)


def add_update(db, userid, storyid, content):
    cur = db.cursor()
    upid = next_updateid(db)
    cur.execute(
        'INSERT INTO updates VALUES(' + str(upid)
        + ',' + str(userid) + ',' + str(storyid) + ')')
    with open('data/' + str(upid) + '.txt', 'w') as f:
        f.write(content)
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

init(db)	
	
db.commit() #save changes
db.close()  #close database
