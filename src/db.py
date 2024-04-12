import math
import functools
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
            uploaded_media text[][],
            post_type text,
            template text,
            post_time timestamp with time zone
        );
        CREATE TABLE IF NOT EXISTS files (
            file_name text,
            file bytea,
            file_id uuid DEFAULT gen_random_uuid()
        );
    """)
    cur.close()

def delete_media(uuid):
    try:
        cur.execute(query)
        db().commit()
        result = cur.fetchall()
        return (True, result)
    except:
        db().rollback()
        cur.close()
    pass

def save_media(media):
    """
    Can only save files up to 1gb (if the file is larger than 1gb you probably don't want it to be compiled into the page)
    returns True for success, False for exceptions
    """
    if len(media) < 1:
        return (True, [])
    file_list = ', '.join(list(map(lambda file: f"('{file.name}', '{file.getvalue().hex()}')", media)))
    query = "INSERT INTO files (file_name, file) VALUES " + file_list + " RETURNING file_name, file_id;"
    cur = db().cursor()
    try:
        cur.execute(query)
        db().commit()
        result = cur.fetchall()
        return (True, result)
    except:
        db().rollback()
        cur.close()
        return (False, [])
        
    cur.close()
    return (True, [])
    
# need to add to uploaded files, not replace
def update_post(original_url):
    def update(title, url, content, tags, media, type, template):
        saved = save_media(media)
        if not saved[0]:
            return False
        saved = list(map(lambda result: [result[0], str(result[1])], saved[1]))
        cur = db().cursor()
        try:
            cur.execute("UPDATE posts SET title = %s, url = %s, content = %s, tags = %s, uploaded_media = uploaded_media || %s, post_type = %s, template = %s WHERE url = %s;", (title, url, content, tags, saved, type, template, original_url))
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
    saved = save_media(media)
    if not saved[0]:
        return False
    saved = list(map(lambda result: [result[0], str(result[1])], saved[1]))
    try:
        cur.execute("INSERT INTO posts VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (title, url, content, tags, saved, type, template, now))
        db().commit()
    except:
        db().rollback()
        cur.close()
        return False
        
    cur.close()
    return True

def get_post(url):
    cur = db().cursor()
    cur.execute("SELECT * FROM posts WHERE url = %s;", (url,))
    result = cur.fetchone()
    cur.close()
    return result

def delete_post(url):
    cur = db().cursor()
    cur.execute("DELETE FROM posts WHERE url = %s;", (url,))
    db().commit()

def get_page(page=1, page_size=5):
    cur = db().cursor()
    cur.execute(f"SELECT * FROM posts ORDER BY post_time DESC LIMIT {page_size} OFFSET {(page - 1) * page_size};")
    result = cur.fetchmany(page_size)
    cur.close()
    return result

def get_total_pages(page_size=5):
    cur = db().cursor()
    cur.execute("SELECT count(*) FROM posts;")
    result = math.ceil(float(cur.fetchone()[0]) / float(page_size))
    cur.close()
    return result if result > 0 else 1
