import os
from base64 import b64decode
from logging import getLogger

import trafilatura
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from newsapi import NewsApiClient
from requests import Request, get
from starlette.exceptions import HTTPException as StarletteHTTPException
from termcolor import colored

from prompts import get_prompt_chain, get_prompt_exercise_chain
from session_handling import SessionData, verifier

logger = getLogger("uvicorn")
app = FastAPI(debug=True)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.middleware("http")
async def dump_headers_middleware(request: Request, call_next):
    headers = dict(request.headers)
    for key, value in headers.items():
        print(colored(f"{key}:", "blue"), colored(f"{value}", "green"))

    response = await call_next(request)
    return response


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    response = await call_next(request)

    return response


@app.get("/texts/{lang}/{level}")
def read_item(
    lang: str = "de",
    level: str = "b2",
    url: str = None,
    session: SessionData = Depends(verifier),
):
    target_url = b64decode(url).decode()
    print(target_url)
    downloaded = trafilatura.fetch_url(target_url)
    main_text = trafilatura.extract(downloaded)
    metadata = trafilatura.extract_metadata(downloaded)
    title = metadata.title
    # print(main_text)

    # Initialize the ChatOpenAI module, load and run the summarize chain

    if not session.chain:
        session.chain = get_prompt_chain()
    summary = session.chain.invoke({"text": main_text})

    return {"text": summary, "title": title}


@app.get("/top-headlines")
async def read_top_headlines():
    """https://newsapi.org/docs/client-libraries/python"""
    # result = newsapi.get_top_headlines()
    params = {"country": "us", "apiKey": os.getenv("NEWS_API_KEY")}
    result = get("https://newsapi.org/v2/top-headlines", params=params).json()
    await verifier.create_session()
    print(result)
    return result["articles"]


@app.get("/news/{category}")
def read_news():
    return {"news": "news"}


@app.get("/exercises/{lang}/{level}")
def exercises(
    lang: str = "de",
    level: str = "B2",
    topic: str = None,
    session: SessionData = Depends(verifier),
):
    if not session.chain_exercise:
        session.chain_exercise = get_prompt_exercise_chain()
    summary = session.chain_exercise.invoke({"text": topic, "level": level})

    data = summary.split("|")
    return {"question": data[0], "answers": data[1:]}
