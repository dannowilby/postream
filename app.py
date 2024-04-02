
import streamlit as st
import psycopg

st.set_page_config(
   page_title="PostStream CMS",
   page_icon="🧊",
)

# @st.cache_resource
# conn = psycopg.connect();


def overview():
    new_post = st.button("Create New")
    if new_post:
        st.text("New entry")

def page_1():
    st.write("Page 1")

def page_2():
    st.write("Page 2")

if st.sidebar.button("Page 1"):
    page_1()

if st.sidebar.button("Page 2"):
    page_2()
