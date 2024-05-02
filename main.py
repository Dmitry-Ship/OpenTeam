
from base import Agent, Team
import os
from dotenv import load_dotenv
load_dotenv(override=True)  

MODEL = os.getenv("OPENAI_MODEL_NAME")

coder = Agent(
    name='developer',
    model=MODEL, 
    system_message="You are a python developer"
)

reviewer = Agent(
    name='code reviewer',
    model=MODEL, 
    system_message="You are a code reviewer, given a code, make sure it is correct, does not contain magic number, missing imports, undefined variables, etc. Return corrected version."
)

team = Team(
    model=MODEL, 
    agents=[coder, reviewer]
)

while True:
    team.start(input("\n> "))


