import streamlit as st

st.set_page_config(
   page_title="PostStream CMS - Overview",
   page_icon="🧊",
)

if st.button("Create new post"):
    st.switch_page("pages/new_post.py")

col1, col2 = st.columns(2)
col1.title("Overview")
col2.selectbox("Sort by", ("Date posted", "View count"))
st.divider()

def post(id):
    col1, col2 = st.columns(2)
    col1.text(id)

    b1, b2 = col2.columns(2)
    
    if b1.button("Analytics", key=id):
        print("pressed")
    if b2.button("Edit", key=f"{id}-2"):
        print("pressed")
    st.divider()

with st.container():
    post("test 1")
    post("test 2")
