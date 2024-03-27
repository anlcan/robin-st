import streamlit as st
import requests
from base64 import b64encode as encode
from random import shuffle
import os

HOST = os.getenv("robin-host", "http://localhost:8000")
# HOST = "https://robin-st-render.onrender.com"

# Streamlit app
st.header('Learn German acb, fuck yeah')
target_url = st.sidebar.text_input("URL", placeholder="Enter URL")
st.sidebar.button("Search & Summarize")
st.sidebar.divider()


# https://docs.streamlit.io/library/advanced-features/caching
@st.cache_data
def get_headlines():
    print("getting headlines...")
    return requests.get(f"{HOST}/top-headlines").json()


@st.cache_data
def get_news(url):
    print(f"fetchin {url}")
    params = {"url": encode(url.encode())}
    return requests.get(f"{HOST}/texts/de/b2", params=params).json()


st.sidebar.subheader("Top Headlines")
with st.spinner("Loading top headlines..."):
    data = get_headlines()
    for article in data:
        if article["title"] != "[Removed]" or article["url"] != "https://removed.com":
            if st.sidebar.button(article["title"][:30] + " ...", help=article['title'], key=article["url"],
                                 type="secondary", use_container_width=True):
                target_url = article["url"]
st.sidebar.divider()
st.sidebar.subheader("Exercises")

for topic in ["modalverben", "präpositionen", "konjunktionen", "adjektive", "adverbien", "pronomen", "verben", ]:
    if st.sidebar.button(topic):
        if 'answer' in st.session_state:
            del st.session_state['answer']
        st.session_state['topic'] = topic

if target_url:
    # if target_url.startswith("http://") or target_url.startswith("https://"):
    #    target_url = target_url.replace("http://", "").replace("https://", "")
    data = get_news(target_url)
    st.subheader(data["title"])
    # st.write(data["text"], )
    st.markdown(
        f"""<p id="myTextField" class="myTextField" onClick="alert()" ondblclick="doubleClickAction()">{data["text"]}</p>"""
        , unsafe_allow_html=True)
    target_url = None


def answer_question():
    print(st.session_state['topic'])
    print(st.session_state['correct_answer'])
    print(st.session_state['answers'])


if 'topic' in st.session_state:
    # if target_url.startswith("http://") or target_url.startswith("https://"):
    #    target_url = target_url.replace("http://", "").replace("https://", "")
    topic = st.session_state['topic']
    st.subheader(f"Exercise on {topic}")

    if "answers" in st.session_state:
        st.write(st.session_state["question"])

        answer = st.radio("Answers", st.session_state["answers"],
                          index=None)  # https://docs.streamlit.io/library/api-reference/widgets/st.radio

        if answer.strip() == st.session_state["correct_answer"].strip():
            st.write("Correct!")
        else:
            st.write("Wrong! -> ", st.session_state["correct_answer"])
        # del st.session_state['topic']
        del st.session_state['answers']
        st.button("Next", key="next")

    else:
        params = {"topic": topic}
        data = requests.get(f"{HOST}/exercises/de/b2", params=params).json()
        st.session_state["correct_answer"] = data["answers"][0]

        st.session_state["question"] = data["question"]
        st.write(st.session_state["question"])

        shuffle(data["answers"])
        st.session_state["answers"] = data["answers"]

        st.radio("Answers", data["answers"], index=None,
                 on_change=answer_question)  # https://docs.streamlit.io/library/api-reference/widgets/st.radio
