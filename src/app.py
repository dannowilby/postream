
import streamlit as st
import psycopg

st.set_page_config(
   page_title="PostStream CMS",
   page_icon="🧊",
)

# @st.cache_resource
# conn = psycopg.connect();

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'overview'

st.switch_page("pages/overview.py")
