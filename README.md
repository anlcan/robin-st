# Streamlit App with OpenAI and Trafilatura

This project is a Streamlit application that uses OpenAI and Trafilatura to fetch and summarize web content.

## Features

- Fetches content from a given URL using Trafilatura.
- Summarizes the fetched content using OpenAI's GPT-3 model.
- The summary is generated in B2 German level language.
- The application is built using Streamlit, making it easy to use and interactive.

## Requirements

The project requires the following Python packages:

- streamlit==1.31.0
- langchain_openai
- openai==1.11.1
- tiktoken==0.5.2
- unstructured==0.11.8
- tabulate==0.9.0
- pdf2image==1.17.0
- pytesseract==0.3.10
- google-search-results==2.4.2
- watchdog
- trafilatura==1.8.0

## Usage

To use the application, you need to provide the OpenAI API Key and the URL of the web page you want to summarize. The application will fetch the content from the URL, summarize it using OpenAI's GPT-3 model, and display the summary.

## Running the Application

To run the application, execute the `streamlit_app.py` script. The application will start and can be accessed via a web browser.

```bash
python streamlit_app.py
```

## Note

Please ensure that you have the necessary permissions and API keys to use OpenAI's GPT-3 model.