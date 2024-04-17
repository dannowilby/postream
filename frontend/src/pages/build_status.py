
import streamlit as st
import subprocess

@st.cache_resource
def execute(cmd, id):
    """Takes a command and an id so that we can memoize the function. We need to do this because Streamlit will rerun this page and run the build script a second time before changing the page otherwise."""
    popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, text=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

st.set_page_config(
   page_title="PostStream CMS - Build",
   page_icon="🧊",
)

st.title("Build")

command = f"cd ../build-server && {st.session_state['build_command']}"
for line in execute(command, st.session_state['build_id']):
    st.text(line)

st.info("Build script has finished executing.")
if st.button("Back to overview", use_container_width=True):
    st.switch_page("pages/overview.py")
