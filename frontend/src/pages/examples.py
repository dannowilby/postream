import streamlit as st
from streamlit_extras.row import row
from streamlit_extras.grid import grid
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.tags import tagger_component
from streamlit_tags import st_tags

st.text_area("what")

st_tags(label="Post tags", value=[], text="Press enter to add more.", suggestions=[], maxtags=-1)


with stylable_container(
    key="test-container",
    css_styles="""
    """
):
    buttons = row([3, 1, 1, 1])
    buttons.empty()
    buttons.button("Delete", use_container_width=True)
    buttons.button("Save", use_container_width=True)
    buttons.button("Post", use_container_width=True)

