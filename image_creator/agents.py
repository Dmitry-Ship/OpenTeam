from base import Agent
from .tools import generate_images_params, ArtGenerationTools
from dotenv import load_dotenv
import os

load_dotenv(override=True)

MODEL = os.getenv("OPENAI_MODEL_NAME")

artgeneration_tools = ArtGenerationTools()

image_creator = Agent(
    name='image_creator',
    model=MODEL,
    tools_mapper={"generate_images": artgeneration_tools.generate_images},
    tools_params=[generate_images_params],
    system_message="""
    Given a topic, write a detailed image description.
    Follow this pattern: [type of shot] of [subject], [description of the subject], [setting], [items in the scene], [lighting], shot on [camera]
    """
)

