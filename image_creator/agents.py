from base import Agent
from .tools import generate_images
from dotenv import load_dotenv
import os

load_dotenv(override=True)

MODEL = os.getenv("OPENAI_MODEL_NAME")

image_creator = Agent(
    name='image analyzer',
    model=MODEL,
    tools=[generate_images],
    system_message="""
    Given a topic, write a detailed image description.
    Follow this pattern: [type of shot] of [subject], [description of the subject], [setting], [items in the scene], [lighting], shot on [camera]
    """
)