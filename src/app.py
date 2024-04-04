
import streamlit as st
import psycopg

st.set_page_config(
   page_title="PostStream CMS",
   page_icon="🧊",
)

# Get database credentials from environment variables
db_user = st.secrets["POSTGRES_USER"]
db_password = st.secrets["POSTGRES_PASSWORD"]
db_host = st.secrets["POSTGRES_HOST"]
db_port = st.secrets["POSTGRES_PORT"]
db_name = st.secrets["POSTGRES_DB"]

print(db_password)

# Connect to the PostgreSQL database
with psycopg.connect(f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}") as conn:
    # Example query
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print("Database version:", record)

    # Close the connection
    conn.close()

# @st.cache_resource
# conn = psycopg.connect();

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'overview'

st.switch_page("pages/overview.py")
