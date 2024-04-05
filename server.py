import os
from base64 import b64decode as decode
from datetime import timedelta

import requests
import trafilatura
from fastapi import Depends
from fastapi import FastAPI
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie
from newsapi import NewsApiClient
from prompts import get_prompt_chain, get_prompt_exercise_chain

from pydantic import BaseModel

class SessionInfo(BaseModel):
    user_id: str
    username: str
    # Add other fields as needed

SESSION_SECRET_KEY = "a_very_secret_key_change_me"
session_backend = InMemoryBackend[SessionInfo]()
session_cookie = SessionCookie[SessionInfo](secret_key=SESSION_SECRET_KEY, backend=session_backend, lifetime=timedelta(hours=1))
def get_session(session_info: SessionInfo = Depends(session_cookie.verify_session)):
    return session_info

@app.get("/texts/{lang}/{level}")
def read_item(lang: str = "de", level: str = "b2", url: str = None, session: SessionInfo = Depends(get_session)):
    target_url = decode(url).decode()
    downloaded = trafilatura.fetch_url(target_url)
    main_text = trafilatura.extract(downloaded)
    metadata = trafilatura.extract_metadata(downloaded)
    title = metadata.title
    # print(main_text)

    # Initialize the ChatOpenAI module, load and run the summarize chain

    chain = get_prompt_chain()
    summary = chain.invoke({"text": main_text})

    return {"text": summary, "title": title}


@app.get("/top-headlines")
def read_top_headlines():
    """ https://newsapi.org/docs/client-libraries/python"""
    # result = newsapi.get_top_headlines()
    params = {"country": "us", "apiKey": os.getenv("NEWS_API_KEY")}
    result = requests.get("https://newsapi.org/v2/top-headlines", params=params).json()
    print(result)
    return result["articles"]


@app.get("/news/{category}")
def read_news():
    return {"news": "news"}


@app.get("/exercises/{lang}/{level}")
def exercises(lang: str = "de", level: str = "B2", topic: str = None, session: SessionInfo = Depends(get_session)):
    chain_exercise = get_prompt_exercise_chain()
    summary = chain_exercise.invoke({"text": topic, "level": level})
    data = summary.split("|")
    return {"question": data[0], "answers": data[1:]}
