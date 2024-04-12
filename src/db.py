import math
import streamlit as st
import psycopg
from datetime import datetime

@st.cache_resource
def db():
    # Get database credentials from environment variables
    db_user = st.secrets["POSTGRES_USER"]
    db_password = st.secrets["POSTGRES_PASSWORD"]
    db_host = st.secrets["POSTGRES_HOST"]
    db_port = st.secrets["POSTGRES_PORT"]
    db_name = st.secrets["POSTGRES_DB"]

    conn = psycopg.connect(f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}", autocommit=True)

    return conn

def get_date():
    cur = db().cursor()
    cur.execute("SELECT current_date;")
    record = cur.fetchone()
    cur.close()
    return record

def init_post_table():
    cur = db().cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            title text,
            url text,
            content text,
            tags text[],
            post_type text,
            template text,
            post_time timestamp with time zone
        );
        CREATE TABLE IF NOT EXISTS files (
            img_name text,
            img bytea
        );
    """)
    cur.close()

def save_file(file):
    """
    Can only save files up to 1gb (if the file is larger than 1gb you probably don't want it to be compiled into the page)
    returns True for success, False for exceptions
    """
    cur = db().cursor()
    try:
        cur.execute(f"INSERT INTO files VALUES ('{file.name}', '{file.getvalue()}');")
        db().commit()
    except:
        db().rollback()
        cur.close()
        return False
        
    cur.close()
    return True

def save_media(media):
    for file in media: # can reduce this to 1 insert call at some point if performance becomes an issue
        if not save_file(file):
            return False
    return True
    

def update_post(original_url):
    def update(title, url, content, tags, media, type, template):
        save_media(media)
        cur = db().cursor()
        try:
            cur.execute("UPDATE posts SET title = %s, url = %s, content = %s, tags = %s, post_type = %s, template = %s WHERE url = %s;", (title, url, content, tags, type, template, original_url))
            db().commit()
        except:
            db().rollback()
            cur.close()
            return False
        return True
    return update

def save_post(title, url, content, tags, media, type, template):
    cur = db().cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_media(media)
    try:
        cur.execute("INSERT INTO posts VALUES (%s, %s, %s, %s, %s, %s, %s);", (title, url, content, tags, type, template, now))
        db().commit()
    except:
        db().rollback()
        cur.close()
        return False
        
    cur.close()
    return True

def get_post(url):
    cur = db().cursor()
    cur.execute(f"SELECT * FROM posts WHERE url = '{url}';")
    result = cur.fetchone()
    cur.close()
    return result

def delete_post(url):
    cur = db().cursor()
    cur.execute(f"DELETE FROM posts WHERE url = '{url}';")
    db().commit()

def get_page(page=1, page_size=5):
    cur = db().cursor()
    cur.execute(f"SELECT * FROM posts ORDER BY post_time DESC LIMIT {page_size};")
    result = cur.fetchmany(page_size);
    cur.close()
    return result

def get_total_pages(page_size=5):
    cur = db().cursor()
    cur.execute("SELECT count(*) FROM posts;")
    result = math.ceil(float(cur.fetchone()[0]) / float(page_size))
    cur.close()
    return result if result > 0 else 1
