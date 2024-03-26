import streamlit as st
import requests
from base64 import b64encode as encode
import os

#HOST = os.getenv("robin-host", "http://localhost:8000")
HOST = "https://robin-st-render.onrender.com"

# Streamlit app
st.header('Translated Text')
target_url = st.sidebar.text_input("URL", placeholder="Enter URL")
st.sidebar.button("Search & Summarize")

st.markdown("""
    <script>
        function doubleClickAction() {
            let textField = document.getElementById('myTextField');
            let selectedText = "";
            if (typeof window.getSelection != "undefined") {
                selectedText = window.getSelection().toString();
            } else if (typeof document.selection != "undefined" && document.selection.type == "Text") {
                selectedText = document.selection.createRange().text;
            }
            if (selectedText) {
                alert("You double-clicked on: " + selectedText);
            }
        }
    </script>

   <style>
   button[kind="primary"] {{
       background: none!important;
       border: none;
       padding: 0!important;
       color: white !important;
       text-decoration: none;
       cursor: pointer;
       border: none !important;
   }}
   button[kind="primary"]:hover {{
       text-decoration: none;
       color: yellow !important;
   }}
   button[kind="primary"]:focus {{
       outline: none !important;
       box-shadow: none !important;
       color: blue !important;
   }}
   </style>
   """,
            unsafe_allow_html=True
            )
with st.spinner("Loading top headlines..."):
    with requests.get(f"{HOST}/top-headlines") as response:
        data = response.json()
        for article in data:
            if article["title"] != "[Removed]" or article["url"] != "https://removed.com":
                if st.sidebar.button(article["title"], key=article["url"]):
                    target_url = article["url"]

if target_url:
    # if target_url.startswith("http://") or target_url.startswith("https://"):
    #    target_url = target_url.replace("http://", "").replace("https://", "")
    params = {"url": encode(target_url.encode())}
    data = requests.get(f"{HOST}/texts/de/b2", params=params).json()

    st.subheader(data["title"])
    # st.write(data["text"], )
    st.markdown(f"""<p id="myTextField" class="myTextField" onClick="alert()" ondblclick="doubleClickAction()">{data["text"]}</p>"""
                ,unsafe_allow_html=True)
    target_url = None

with st.sidebar:
    st.caption("")
