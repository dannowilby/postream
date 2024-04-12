import streamlit as st
from streamlit_extras.row import row
from streamlit_tags import st_tags

import db

st.set_page_config(
   page_title="PostStream CMS - Create new post",
   page_icon="🧊",
)

new_post = st.session_state['editing'] == ''

current_post = ("", "", "", [], "", "", "")
if not new_post:
    current_post = db.get_post(st.session_state['editing'])

if st.button("Back to overview"):
    st.switch_page("pages/overview.py")

st.title("New Post" if new_post else "Post")

title = st.text_input("Title", value=current_post[0])

url = st.text_input("URL", value=current_post[1])

post_contents = st.text_area("Contents", value=current_post[2])

tag_list = st_tags(label="Tags", value=current_post[3], text="Press enter to add more.", suggestions=[], maxtags=-1)

files = st.file_uploader("Media", accept_multiple_files=True)

# add a field specifying uploaded media
# might need to rethink this part

project_type = st.selectbox("Post type", ("Article", "Project", "Art"))

template = st.text_input("Template", value=current_post[5])

st.divider()

b = row([1, 1, 1])
b.empty()

escape = "Back to overview" if new_post else "Delete"
if b.button(escape, use_container_width=True):
    if new_post:
        st.switch_page("pages/overview.py")
    else:
        db.delete_post(url)
        st.session_state['page'] = 1
        st.switch_page("pages/overview.py")
        

# can be cleaner, will fix in the future
if b.button("Save", type="primary", use_container_width=True):
    save_func = db.save_post if new_post else db.update_post
    success = save_func(title, url, post_contents, tag_list, files, project_type, template)
    if success:
        st.session_state['page'] = 1
        st.switch_page("pages/overview.py")
    else:
        st.error("There was an error saving the post. Make sure all fields are well formatted and all services are running.")