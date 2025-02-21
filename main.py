import streamlit as st
from utils import (
    get_groq_api_key, get_url_input, validate_input, load_content, summarize_content
)
from langchain_groq import ChatGroq
from langchain import PromptTemplate

# Streamlit UI setup
st.set_page_config(page_title="🔍Langchain: Summarize text from YouTube or Websites", page_icon="🦜")
st.title("🦜Langchain: Summarize text from YT or Website")
st.subheader('Summarize URL')

# API Key and URL input
groq_api_key = get_groq_api_key()
generic_url = get_url_input()

# LLM model and prompt setup
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)
prompt_template = """ 
Provide a summary of the following content in 300 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarize the content from YT or Website"):
    if validate_input(groq_api_key, generic_url):
        try:
            with st.spinner("Waiting...."):
                # Load and Summarize content
                docs = load_content(generic_url)
                if docs:
                    output_summary = summarize_content(llm, docs, prompt)
                    st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception: {e}")
