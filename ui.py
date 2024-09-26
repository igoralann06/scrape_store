import streamlit as st
from pathlib import Path
from main import scrape_store

st.title("Uber Eats store")
col1, col2 = st.columns([3, 1])
store_url = ""

with col1:
    store_url = st.text_input("Enter the url of store:", "https://www.ubereats.com/store/sergios-west-kendall-lakes-%26-london-square/yodiLTWiQ1Wr1wb55iE4sQ?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMldlc3QlMjBLZW5kYWxsJTIwQmFwdGlzdCUyMEhvc3BpdGFsJTIyJTJDJTIycmVmZXJlbmNlJTIyJTNBJTIyaGVyZSUzQXBkcyUzQXBsYWNlJTNBODQwang3cHMtMmViNmMyZWZkMTMwMDA3MTg0Yzk4MjU1NDk2ZjZhZDIlMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyaGVyZV9wbGFjZXMlMjIlMkMlMjJsYXRpdHVkZSUyMiUzQTI1LjY3ODQ2JTJDJTIybG9uZ2l0dWRlJTIyJTNBLTgwLjQ1NTYlN0Q%3D")

with col2:
    if st.button("Run"):
        scrape_store(store_url)


def list_files_and_folders(folder):
    items = []
    for item in Path(folder).iterdir():
        items.append(item)
    return items

if 'folder_path' in st.session_state:
    items = list_files_and_folders(st.session_state.folder_path)
else:
    items = list_files_and_folders("./resources")

if 'folder_path' in st.session_state:
    if st.button(" Go Up"):
        st.session_state.folder_path = str(Path(st.session_state.folder_path).parent)
        st.rerun()
    
for item in items:
    if item.is_dir():
        if st.button(f" {item.name}"):
            st.session_state.folder_path = str(item)
            st.rerun()
    else:
        file_link = f'<a href="./{item}" download>{item.name}</a>'
        st.markdown(file_link, unsafe_allow_html=True)