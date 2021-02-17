from flask import Flask 

from flask import abort, send_file, render_template, request, redirect
from flask_autoindex import AutoIndex, Directory
import os

import sqlite3
from sqlite3 import Error

from PIL import Image

app = Flask(__name__)

def get_reading_comics():
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT filename FROM comics WHERE status = '1'")

    comics = []
    rows = cur.fetchall()
    for row in rows:
        comics.append(row[0])

    return comics

def is_comic_reading(ent):
    if isinstance(ent, Directory):
        return False
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM comics WHERE filename LIKE ? AND status = '1'", ("%"+ent.name+"%",))

    rows = cur.fetchall()

    if len(rows) > 0:
        return True
    else:
        return False

def is_comic_read(ent):
    if isinstance(ent, Directory):
        return False
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM comics WHERE filename LIKE ? AND status = '2'", ("%"+ent.name+"%",))

    rows = cur.fetchall()

    if len(rows) > 0:
        return True
    else:
        return False


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def check_filename_status(conn,filename):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM comics WHERE filename = ?" , (filename,))

    rows = cur.fetchall()

    if len(rows) > 0:
        return rows[0]
    else:
        return False

def mark_as_reading(conn, comic):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''INSERT INTO comics(filename,status,page) VALUES(?,?,?) '''
    print("inseting {}".format(sql))
    cur = conn.cursor()
    try:
        cur.execute(sql, comic)
    except Error as e:
        print(e)
    return cur.lastrowid

def update_page(conn, comic):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE comics
              SET page = ?, STATUS = 1
              WHERE filename = ?'''
    cur = conn.cursor()
    cur.execute(sql, comic)
    conn.commit()

def end_comic(conn, comic):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE comics
              SET status = 2
              WHERE filename = ?'''
    cur = conn.cursor()
    cur.execute(sql, comic)
    conn.commit()

def comic_unread(conn, comic):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE comics
              SET status = 0
              WHERE filename = ?'''
    cur = conn.cursor()
    cur.execute(sql, comic)
    conn.commit()

def init_db():
    sql = '''CREATE TABLE comics(filename TEXT,status INT,page INT)'''
    conn = create_connection(db_file)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


ppath = "/comics/" # update your own parent directory here
files_index = AutoIndex(app, ppath, add_url_rules=False)
files_index.add_icon_rule('contrast.png', rule=is_comic_reading)
files_index.add_icon_rule('tick.png', rule=is_comic_read)
db_file = r"/usr/src/app/sqlite.db"

@app.route('/')
@app.route('/index')
def index():
    if not os.path.isfile(db_file):
        init_db()
    # TODO : List currently reading comics
    return render_template('index.html',comics=get_reading_comics())

@app.route('/update_path')
def update():
    path = request.args.get('path')
    page = request.args.get('page')

    print("updateing path {} {}".format(path,page))
    conn = create_connection(db_file)
    with conn:
        update_page(conn, (page,path))
    return '0'

@app.route('/end_comic')
def end():
    path = request.args.get('path')

    print("ending comic {}".format(path))
    conn = create_connection(db_file)
    with conn:
        end_comic(conn, (path,))
    return '0'

@app.route('/mark_unread')
def mark_unread():
    path = request.args.get('path')

    print("marking comic as unread {}".format(path))
    conn = create_connection(db_file)
    with conn:
        comic_unread(conn, (path,))
    return redirect(request.referrer)


# Custom indexing
@app.route('/comics')
@app.route('/comics/')
@app.route('/comics/<path:path>')
def autoindex(path='.'):
    BASE_DIR = '/comics/'
    TEMP_DIR = '/usr/src/app/project/static/temp/'
    READING = 1
    conn = create_connection(db_file)

    print(path)
    if path[-3:] == 'cbr':
        print("extracting {}".format(BASE_DIR+path))
        print("Clearing Temp Directory")
        os.system('rm -rf {}*'.format(TEMP_DIR))
        print("Extracting comic")
        os.system('unrar e "{}" {}'.format(BASE_DIR+path,TEMP_DIR))
        print("Checking if we are reading")
        result = check_filename_status(conn,path)
        if not result:
            print("Not reading")
            with conn:
                print(mark_as_reading(conn,(path,READING,0)))
                page = 0
        else:
            page = result[2]
        print(page)
        listing = sorted(os.listdir(TEMP_DIR))
        files = []
        for filename in listing:
            if filename.endswith('png') or filename.endswith('jpg') or filename.endswith('jpeg'):
                print(TEMP_DIR + filename)
                img = Image.open(TEMP_DIR+filename)
                print(img.height)
                files.append({'filename':filename,'height':img.height,'width':img.width})
        return render_template('view.html',files=files,page=page,path=path)
    elif path[-3:] == 'cbz':
        print(path)
        print("extracting {}".format(BASE_DIR+path))
        print("Clearing Temp Directory")
        os.system('rm -rf {}*'.format(TEMP_DIR))
        print("Extracting comic")
        os.system('unzip -j "{}" -d {}'.format(BASE_DIR+path,TEMP_DIR))
        print("Checking if we are reading")
        result = check_filename_status(conn,path)
        if not result:
            print("Not reading")
            with conn:
                print(mark_as_reading(conn,(path,READING,0)))
                page = 0
        else:
            page = result[2]
        print(page)

        listing = sorted(os.listdir(TEMP_DIR))
        files = []
        for filename in listing:
            if filename.endswith('png') or filename.endswith('jpg') or filename.endswith('jpeg'):
                print(TEMP_DIR + filename)
                img = Image.open(TEMP_DIR+filename)
                print(img.height)
                files.append({'filename':filename,'height':img.height,'width':img.width})
        return render_template('view.html',files=files,page=page,path=path)
    else:
        return files_index.render_autoindex(path)


@app.template_filter('get_comic_name')
def reverse_filter(s):
    splitter = s.split("/")[-1]
    return splitter[:-4]
