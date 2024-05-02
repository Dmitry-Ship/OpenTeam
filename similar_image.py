from base import Agent
from tools.art_generation import generate_image
from dotenv import load_dotenv
import os

load_dotenv(override=True)

MODEL = os.getenv("OPENAI_MODEL_NAME")
VISION_MODEL = os.getenv("OPENAI_VISION_MODEL_NAME")

image_analyzer = Agent(
    name='image analyzer',
    model=VISION_MODEL,
    system_message="""
    You are an image analyzer. Given an image url, return description of the image. Follow this pattern: [type of shot] of [subject], [setting], [items in the scene], [lighting], shot on [camera]
    """
)

while True:
    url = input("\n> ")
    message = [
        {"type": "text", "text": "What’s in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": url,
          },
        },
      ]
    image_analyzer.reset()
    response = image_analyzer.chat(message)
    result = generate_image(response)
    print(result)
