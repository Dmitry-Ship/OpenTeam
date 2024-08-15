from base import Agent
from .tools import retreive_youtube_transcription, retreive_youtube_transcription_params
from dotenv import load_dotenv
import os

load_dotenv(override=True)

MODEL = os.getenv("OPENAI_MODEL_NAME")

youtube_transcriber = Agent(
    name='youtube_transcriber',
    model=MODEL,
    tools_params=[retreive_youtube_transcription_params],
    tools_mapper={"retreive_youtube_transcription": retreive_youtube_transcription},
    system_message="""
    Your goal is to answer questions about a given youtube video.
    """
)
