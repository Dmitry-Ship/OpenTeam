from .tools import retreive_youtube_transcription
from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI
load_dotenv(override=True)

MODEL = os.getenv("OPENAI_MODEL_NAME")

@st.cache_resource
def get_transcription(url):
    return retreive_youtube_transcription(url)

def main():
    st.title("Youtube Transcriber")

    url = st.text_input("URL")
    
    if url == "":
        return
    
    if "messages" not in st.session_state:
        transcript = get_transcription(url)
        st.session_state["messages"] = [
            {"role": "system", "content": f"""
        Your goal is to answer questions about transcript of a youtube video.

        Transcript:
        {transcript}
        """},
            {"role": "assistant", "content": "How can I help you?"}
        ]

    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        client = OpenAI(base_url=os.getenv("BASE_URL"))
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model=MODEL, messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)


