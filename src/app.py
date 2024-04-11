
import streamlit as st
import db

st.set_page_config(
   page_title="PostStream CMS",
   page_icon="🧊",
)

# current page for pagination on overview
if 'page' not in st.session_state:
    st.session_state['page'] = 1
# the current post you are editing, selected by the url(empty string for new post)
if 'editing' not in st.session_state:
    st.session_state['editing'] = ''

db.init_post_table();

print(db.get_total_pages())

st.switch_page("pages/overview.py")
