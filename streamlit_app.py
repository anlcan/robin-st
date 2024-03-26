import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import trafilatura

# Streamlit app
st.subheader('Last Week In...')


def get_summary(target_url):
    # loader = UnstructuredURLLoader(urls=[target_url], ssl_verify=False, headers={
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
    # data = loader.load()
    downloaded = trafilatura.fetch_url(target_url)
    main_text = trafilatura.extract(downloaded)
    print(main_text)
    # Initialize the ChatOpenAI module, load and run the summarize chain
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
    # prompt_template = """Write a summary of the following in 100-150 words in B2 German level:
    #
    #             {text}
    #
    #         """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Write a summary of the following in 200-250 words in B2 German levelm break it into :"),
        ("user", "{text}")
    ])

    chain = prompt | llm | StrOutputParser()
    summary = chain.invoke({"text": main_text})
    return summary



# Get OpenAI API key, Serper API key, number of results, and search query
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", value="", type="password")
    st.caption("*Search & Summarize: Uses Serper & OpenAI APIs, summarizes each search result.*")
    url = st.text_input("URL", value="https://johnjago.com/great-docs/?utm_source=tldrnewsletter")
    # If 'Search & Summarize' button is clicked
    if st.button("Search & Summarize"):
        # Validate inputs
        if not openai_api_key.strip() or not url:
            st.error(f"Please provide the missing fields.")
        else:
            try:
                with st.spinner("Please wait..."):
                    summary = get_summary(url)
                    st.write(summary)

            except Exception as e:
                st.exception(f"Exception: {e}")
# search_query = st.text_input("Search Query", label_visibility="collapsed")


if __name__ == "__main__":
    print(get_summary("https://johnjago.com/great-docs/?utm_source=tldrnewsletter"))
