import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from langchain.chains import LLMChain
from langchain import PromptTemplate
import validators, streamlit as st
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


## Streamlit initializing
st.set_page_config(page_title="🔍Langchain: Summarize text from YouTube or Websites", page_icon="🦜")
st.title("🦜Langchain: Summarize text from YT or Website")
st.subheader('Summarize URL')

# Get the Groq API Key and URL field to be Summarized
with st.sidebar:
    groq_api_key = st.text_input("GROQ API KEY", value="", type="password")

generic_url = st.text_input("URL", label_visibility="collapsed")

## The LLM model
llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

prompt_template = """ 
Provide a summary of the following content in 300 words:
Content: {text}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarize the content from YT or Website"):
    # Validate all the input
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the info to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL for Summarization.")
    else:
        try:
            with st.spinner("Waiting...."):
                ## Loading the website data
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify=False, 
                        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs = loader.load()

                # Check if documents were loaded successfully
                if not docs:
                    st.error("Failed to load content from the URL. Please try a different link.")
                else:
                    ## Chain for summarization
                    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                    output_summary = chain.run(docs)

                    st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception: {e}")
