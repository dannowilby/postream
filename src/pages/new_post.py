import streamlit as st
from streamlit_extras.row import row
from streamlit_tags import st_tags

st.set_page_config(
   page_title="PostStream CMS - Create new post",
   page_icon="🧊",
)

if st.button("Back to overview"):
    st.switch_page("pages/overview.py")

st.title("New post")

title = st.text_input("Post title")

post_contents = st.text_area("Post contents")

project_type = st.selectbox("Post type", ("Article", "Project"))

st_tags(label="Post tags", value=[], text="Press enter to add more.", suggestions=[], maxtags=-1)

st.file_uploader("Post media", accept_multiple_files=True)

st.divider()

b = row([1, 1, 1])
delete = b.button("Delete", use_container_width=True)
save = b.button("Save", use_container_width=True)
post = b.button("Post", use_container_width=True)
