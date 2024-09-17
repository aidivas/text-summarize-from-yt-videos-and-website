import validators
import streamlit as st
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# Function to get the Groq API key input
def get_groq_api_key():
    with st.sidebar:
        groq_api_key = st.text_input("GROQ API KEY", value="", type="password")
    return groq_api_key

# Function to get URL input
def get_url_input():
    return st.text_input("URL", label_visibility="collapsed")

# Function to validate the input
def validate_input(groq_api_key, generic_url):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the necessary information to get started")
        return False
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL for summarization.")
        return False
    return True

# Function to load content from the URL or YouTube
def load_content(url):
    try:
        if "youtube.com" in url:
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        else:
            loader = UnstructuredURLLoader(
                urls=[url],
                ssl_verify=False,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
            )
        docs = loader.load()
        if not docs:
            st.error("Failed to load content from the URL. Please try a different link.")
        return docs
    except Exception as e:
        st.exception(f"Error loading content: {e}")
        return None

# Function to summarize content
def summarize_content(llm, docs, prompt):
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
    return chain.run(docs)
