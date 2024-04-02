import streamlit as st

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

st.file_uploader("Post media", accept_multiple_files=True)

st.subheader("Preview")
st.divider()

st.title(title)
st.markdown(post_contents)

st.divider()

b1, b2, b3 = st.columns(3)
delete = b1.button("Delete")
save = b2.button("Save")
post = b3.button("Post")
