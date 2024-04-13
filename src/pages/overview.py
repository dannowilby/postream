import streamlit as st
from streamlit_extras.row import row
import db

st.set_page_config(
   page_title="PostStream CMS - Overview",
   page_icon="🧊",
)

st.title("Overview")
a = row([1, 1])
if a.button("Create new post", use_container_width=True):
    st.session_state['editing'] = ''
    st.switch_page("pages/new_post.py")
if a.button("Run build script", use_container_width=True):
    pass
    
st.divider()

def post(entry):
    b = row([5, 1])
    date = entry[7]
    b.text(f"{entry[0]}\nCreated {date.year}-{date.month}-{date.day}")
    if b.button("Edit", key=entry[0], use_container_width=True):
        st.session_state['editing'] = entry[1]
        st.switch_page("pages/new_post.py")
        
    st.divider()

with st.container():
    for entry in db.get_page(page=st.session_state['page']):
        post(entry)


total_pages = db.get_total_pages()

def next_enabled():
    return not st.session_state['page'] < total_pages
def prev_enabled():
    return not st.session_state['page'] > 1

def next_page():
    st.session_state['page'] += 1
def prev_page():
    st.session_state['page'] -= 1

c = row([4, 1, 1, 1, 4])
c.empty()
c.button("<", disabled=prev_enabled(), on_click=prev_page)
c.text(f"{st.session_state['page']} / {total_pages}")
c.button("\>", disabled=next_enabled(), on_click=next_page)
c.empty()
