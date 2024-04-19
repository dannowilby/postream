
import streamlit as st
import state

st.set_page_config(
   page_title="PostStream CMS",
   page_icon="🧊",
)

state.initialize()

st.switch_page("pages/overview.py")


