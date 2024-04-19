
import streamlit as st
import requests
import os
import state

st.set_page_config(
   page_title="PostStream CMS - Build",
   page_icon="🧊",
)

state.initialize()

st.title("Build")

session = requests.Session()

host = os.environ.get("CONTENT_HOST")
port = os.environ.get("CONTENT_PORT")

with session.get(f"http://{host}:{port}", headers=None, stream=True) as res:
    for line in res.iter_lines():
        if line:
            st.write(line.decode('UTF-8'))

st.info("Build script has finished executing.")
if st.button("Back to overview", use_container_width=True):
    st.switch_page("pages/overview.py")
