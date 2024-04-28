from openai import OpenAI
from dotenv import load_dotenv
from base import Agent, Team
import os

load_dotenv(override=True)  # take environment variables from .env.

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
)

MODEL = os.getenv("OPENAI_MODEL_NAME")

coder = Agent(
    name='developer',
    client=client, 
    model=MODEL, 
    system_message="You are a python developer"
)

reviewer = Agent(
    name='code reviewer',
    client=client, 
    model=MODEL, 
    system_message="You are a code reviewer"
)

team = Team(
    client=client, 
    model=MODEL, 
    agents=[coder, reviewer]
)

while True:
    team.start(input("\n> "))


