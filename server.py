import os

import requests
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import trafilatura
from base64 import b64decode as decode

from newsapi import NewsApiClient

app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Write a summary of the following in 200-250 words in B2 German level break it into"),
    ("system", "the output text will be rendered in html so wrap the paragraps in <p> tags"),
    ("user", "{text}")
])
chain = prompt | llm | StrOutputParser()


newsapi = NewsApiClient(os.getenv("NEWS_API_KEY"))

@app.get("/texts/{lang}/{level}")
def read_item(lang: str = "de" ,level:str = "b2", url: str = None):
    target_url = decode(url).decode()
    downloaded = trafilatura.fetch_url(target_url)
    main_text = trafilatura.extract(downloaded)
    metadata = trafilatura.extract_metadata(downloaded)
    title = metadata.title
    # print(main_text)

    # Initialize the ChatOpenAI module, load and run the summarize chain

    summary = chain.invoke({"text": main_text})

    return {"text":summary, "title": title}


@app.get("/top-headlines")
def read_top_headlines():
    """ https://newsapi.org/docs/client-libraries/python"""
    #result = newsapi.get_top_headlines()
    params = {"country": "us", "apiKey": os.getenv("NEWS_API_KEY")}
    result = requests.get("https://newsapi.org/v2/top-headlines", params=params).json()
    print(result)
    return result["articles"]
@app.get("/news/{category}")
def read_news():
    return {"news": "news"}