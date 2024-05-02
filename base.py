import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)  # take environment variables from .env.

class Agent:
    def __init__(self, name, model, system_message="", tools=[]):
        self.chat_history = [
            {
                "role": "system",
                "content": system_message
            }
        ]
        self.system_message = system_message
        self.name = name
        self.model = model
        self.llm = OpenAI(
            base_url=os.getenv("BASE_URL"),
        )
        self.tools = tools

    def chat(self, prompt):
        self.chat_history += [{
            "role": "user",
            "content": prompt,
        }]

        response = self.llm.chat.completions.create(
            temperature=0,
            messages=self.chat_history,
            model=self.model,
            stream=True,
        )

        collected_chunks = ""
        for chunk in response:
            message = chunk.choices[0].delta.content
            if message is not None:
                print(message, end='')
                collected_chunks += message  # save the event response
        print("\n")
        self.chat_history += [{
            "role": "assistant",
            "content": collected_chunks,
        }]

        return collected_chunks
    
    def update_system_message(self, new_system_message):
        self.chat_history[0] = {
            "role": "system",
            "content": new_system_message
        }
        self.system_message = new_system_message

    def reset(self):
        self.chat_history = [
            {
                "role": "system",
                "content": self.system_message
            }
        ]
    
class Team:
    def __init__(self, model, agents):
        self.agents_map = {}
        for agent in agents:
            self.agents_map[agent.name] = agent
        agent_names = [agent.name for agent in agents]
        self.model = model
        self.manager = Agent(
            name='manager',
            model=model, 
            system_message=f""""""
        )

        self.update_system_message(agent_names)

    def update_system_message(self, eligible_agents):
        self.manager.update_system_message(f"""
            You are a managing team. Available agents: {eligible_agents}
            Given a message, return the name of the agent that should answer this message. Dont return the same agent twice.
            Dont answer the message youself.
            Only respond in this format:
            {{
                "name": "...",
            }}
            """)

    def start(self, problem):
        called_agents = {}
        while True:
            if len(called_agents) == len(self.agents_map):
                break
            if len(called_agents) > 0:
                eligible_agents = [agent for agent in self.agents_map if agent not in called_agents]
                self.update_system_message(eligible_agents)

            response = self.manager.chat(f"Which agent shoud respond to this? {problem} Respond in this format: {{\"name\": \"\"}}")

            next_agent = json.loads(response).get("name")

            if next_agent in self.agents_map:
                problem = self.agents_map[next_agent].chat(problem)

                called_agents[next_agent] = next_agent            
