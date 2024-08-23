from base import Agent
from .tools import retreive_youtube_transcription
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv(override=True)

MODEL = os.getenv("OPENAI_MODEL_NAME")

@st.cache_resource
def get_agent(url):
    transcript = retreive_youtube_transcription(url) 
    youtube_transcriber = Agent(
        name='youtube_transcriber',
        model=MODEL,
        system_message=f"""
        Your goal is to answer questions about transcript of a youtube video.

        Transcript:
        {transcript}
        """
    )
    return youtube_transcriber

def main():
    st.title("Youtube Transcriber")

    url = st.text_input("URL")
    
    if url:
        youtube_transcriber = get_agent(url)

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            msg = youtube_transcriber.chat(prompt)
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)


