import streamlit as st
from streamlit_extras.row import row

st.set_page_config(
   page_title="PostStream CMS - Overview",
   page_icon="🧊",
)

st.title("Overview")
a = row([1, 1])
if a.button("Create new post", use_container_width=True):
    st.switch_page("pages/new_post.py")
if a.button("Run build script", use_container_width=True):
    print("test")
    
st.divider()

def post(id):
    b = row([5, 1])
    b.text("Why I made my own CMS\nPosted on 2024-10-03")
    b.button("Edit", key=id, use_container_width=True)

    st.divider()

with st.container():
    post("test 1")
    post("test 2")


c = row([4, 1, 1, 1, 4])
c.empty()
c.button("<")
c.text("1 / 1")
c.button("\>")
c.empty()
