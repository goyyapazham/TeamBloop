import sqlite3
import csv

f="data/users.db"



def db_f(func):
    def wrapped(*args, **kwargs):  # handles locking and weird db issues
        try:
            if isinstance(args[0], sqlite3.Connection):  # db is in args
                return func(*args, **kwargs)
        except IndexError:
            pass
        db = sqlite3.connect(f)
        v = func(db, *args, **kwargs)
        db.close()
        return v
    return wrapped

@db_f
def init(db):
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, password TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS stories (id INTEGER, title TEXT, latestid INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS updates (id INTEGER, userid INTEGER, storyid INTEGER, content TEXT)")
    cur.execute("INSERT INTO stories VALUES (-1, '', -1)")
    cur.execute("INSERT INTO updates VALUES (-1, -1, -1, '')")
    cur.execute("INSERT INTO users VALUES (-1, '', '')")
    # need base, unused data to do next id functions
    db.commit()


@db_f
def query(db, q):  # for external use, not optimized
    ret = db.cursor().execute(q)
    db.commit()
    for i in ret:
        return i[0]
		
@db_f
def queryL(db, q):  # for external use, not optimized
	ret = db.cursor().execute(q)
	db.commit()
	r = []
	for i in ret:
		r += [i]
	return r
	
@db_f
def add_user(db, user, password):
    cur = db.cursor()
    q = "INSERT INTO users VALUES (%d, \'%s\', \'%s\')"%(next_userid(db), user, password)
    print q
    cur.execute(q)
    db.commit()


@db_f
def get_userid(db, user):
    id_holder = db.cursor().execute('SELECT id FROM users WHERE username = "' + user + '"')
    L = []
    for row in id_holder:
        return row[0] 
    
	

@db_f
def get_stories(db, userid, viewing_on=True):
    cur = db.cursor()
    q = '''SELECT updates.storyid FROM updates WHERE
        updates.userid = ''' + str(userid)
    res = cur.execute(q)
    edited = [i[0] for i in res]
    if viewing_on:
        return sorted(edited)
    else:
        total = set(range(next_storyid(db)))
        return sorted(total - set(edited))  # set subtraction is cool


@db_f
def add_story(db, title, userid, init_update):
    cur = db.cursor()
    newid = next_storyid(db)
    newupid = next_updateid(db)
    cur.execute(
        'INSERT INTO stories VALUES (' + str(newid)
        + ', "' + title + '",' + str(newupid) + ')')
    db.commit()
    add_update(db, userid, newid, init_update)


@db_f
def add_update(db, userid, storyid, content):
    cur = db.cursor()
    upid = next_updateid(db)
    cur.execute("INSERT INTO updates VALUES (%d, %d, %d, \'%s\')"%(upid, userid, storyid, content))
    db.commit()


@db_f
def get_title(db, storyid):
    title_holder = db.cursor().execute(
        'SELECT title FROM stories WHERE id = ' + str(storyid))
    for i in title_holder:
        return i[0]


@db_f
def get_all_users(db):
    cur = db.cursor()
    res = cur.execute("SELECT * FROM users")
    L = []
    for row in res:
        L += [[row[1],row[2]]]
    db.commit()
    return L


@db_f
def edited_by(db, storyid, userid):
    return storyid in get_stories(db, userid)


@db_f
def get_latest_update(db, storyid):
    c_h = db.cursor().execute(
        'SELECT latestid FROM stories WHERE id = '+ str(storyid))
    for i in c_h: #  c_h should be a singleton list, ids are unique
        return i[0]


@db_f
def get_all_updates(db, storyid):
    return [i[0] for i in db.cursor().execute('SELECT id FROM updates WHERE storyid = ' + str(storyid))]


@db_f
def get_update(db, updateid):
    return [i[0] for i in db.cursor().execute('SELECT content FROM updates WHERE storyid = ' + str(updateid))]


@db_f
def get_author(db, storyid):
    updates = get_all_updates(db, storyid)
    first_update = min(updates)
    r = db.cursor().execute('SELECT userid FROM updates WHERE id = ' + str(first_update))
    for i in r:
        return i[0]


@db_f
def next_updateid(db):
    uids = [i[0] for i in db.cursor().execute(
        'SELECT id FROM updates')]
    return max(uids) + 1


@db_f
def next_storyid(db):
    sids = [i[0] for i in db.cursor().execute(
        'SELECT id FROM stories')]
    return max(sids) + 1


@db_f
def next_userid(db):
    uids = [i[0] for i in db.cursor().execute(
        'SELECT id FROM users')]
    return max(uids) + 1


try:
    init()
except:
    pass
