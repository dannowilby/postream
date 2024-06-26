import streamlit as st
import db

def initialize():
    # current page for pagination on overview
    if 'page' not in st.session_state:
        st.session_state['page'] = 1
    # the current post you are editing, selected by the url(empty string for new post)
    if 'editing' not in st.session_state:
        st.session_state['editing'] = ''

    if 'build_id' not in st.session_state:
        st.session_state['build_id'] = 1

    db.init_post_table();
