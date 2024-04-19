import math
import functools
import streamlit as st
import psycopg
from datetime import datetime
import os

@st.cache_resource
def db():
    # Get database credentials from environment variables
    # move away from using streamlit secrets because they're a bitch to integrate
    db_user = os.environ.get("POSTGRES_USER") # st.secrets["POSTGRES_USER"]
    db_pass = os.environ.get("POSTGRES_PASSWORD") # st.secrets["POSTGRES_PASSWORD"]
    db_host = os.environ.get("POSTGRES_HOST") # st.secrets["POSTGRES_HOST"]
    db_port = os.environ.get("POSTGRES_PORT") # st.secrets["POSTGRES_PORT"]
    db_name = os.environ.get("POSTGRES_DB") # st.secrets["POSTGRES_DB"]

    connection_details = f"dbname={db_name} user={db_user} password={db_pass} host={db_host} port={db_port}"
    print(connection_details)
    conn = psycopg.connect(connection_details, autocommit=True)

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

def delete_media(url, uploaded, uuid):
    # get an updated list of linked media without the file that we are deleting
    updated_post_media = list(filter(lambda file: file[1] != uuid, uploaded))
    cur = db().cursor()
    try:
        # update the post with the updated media list
        cur.execute("UPDATE posts SET uploaded_media = %s WHERE url = %s;", (updated_post_media, url))
        # remove the file from the file table
        cur.execute("DELETE FROM files WHERE file_id = %s;", (uuid))
        db().commit()
        cur.close()
        return True
    except:
        db().rollback()
        cur.close()
    return False

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

# Todo: delete all associated media with the post
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
