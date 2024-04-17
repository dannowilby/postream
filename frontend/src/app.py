
import streamlit as st
import db

st.set_page_config(
   page_title="PostStream CMS",
   page_icon="🧊",
)

with open("build-server.sh", "r") as file:
    st.session_state['build_id'] = 0
    st.session_state['build_command'] = file.read()
  
# current page for pagination on overview
if 'page' not in st.session_state:
    st.session_state['page'] = 1
# the current post you are editing, selected by the url(empty string for new post)
if 'editing' not in st.session_state:
    st.session_state['editing'] = ''

db.init_post_table();

st.switch_page("pages/overview.py")
