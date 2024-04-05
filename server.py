import os
from datetime import timedelta
from fastapi import Depends
from fastapi_sessions import SessionCookie, SessionInfo
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, SessionInfo
from fastapi_sessions.session_verifier import SessionVerifier

import requests
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import trafilatura
from base64 import b64decode as decode

from newsapi import NewsApiClient

app = FastAPI()

SESSION_SECRET_KEY = "a_very_secret_key_change_me"
session_backend = InMemoryBackend[SessionInfo]()
session_cookie = SessionCookie(
    secret_key=SESSION_SECRET_KEY,
    session_backend=session_backend,
    max_age=timedelta(hours=1)
)

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Write a summary of the following in 200-250 words in B2 German level break it into"),
    ("system", "the output text will be rendered in html so wrap the paragraps in <p> tags"),
    ("user", "{text}")
])
chain = prompt | llm | StrOutputParser()

prompt_exercise = ChatPromptTemplate.from_messages([
    ("system", """
    You are an excellent German teacher, and you generate exercises for your students.
    You always create exercises that are challenging and engaging for your students.
    You create exercises that are tailored to the level of your students, which is {level} in this case. 
    You keep the sentences challenging but understandable, use the vocabulary that is appropriate for the level.
    you generate one sentence per exercise unless specified otherwise. 
    The exercises are fill-in-the-blank exercises.
    The text generated should be in German.
    The text generated should be in the CSV format, where first colum is the exercise, the second colum is the correct answer, 
    and add three columns with wrong answers. use | as the delimiter.
    Mark the blank with dashes: ___
    don't start with the column description
    
    Here is a bad example, becuase it is short and lacks context:
    Ich ___ am Wochenende ins Kino. | gehe | gehen | geht | gegangen
    
    Here area a good example:
    Unser Lehrer erklärt die Grammatik ___ , damit wir sie besser verstehen können |"geduldig" | "schnell" |"laut" |"aufgeregt"

    
    """),
    ("user", "create an exercise on the following topic: {text}")
])
chain_exercise = prompt_exercise | llm | StrOutputParser()

newsapi = NewsApiClient(os.getenv("NEWS_API_KEY"))


@app.middleware("http")
async def add_session_middleware(request: Request, call_next):
    response = await call_next(request)
    await session_cookie.attach_to_response(request, response)
    return response

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
    summary = chain_exercise.invoke({"text": topic, "level": level})
    data = summary.split("|")
    return {"question": data[0], "answers": data[1:]}
