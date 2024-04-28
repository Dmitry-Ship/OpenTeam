import json

class Agent:
    def __init__(self, name, client, model, system_message=""):
        self.chat_history = [
            {
                "role": "system",
                "content": system_message
            }
        ]
        self.name = name
        self.model = model
        self.client = client

    def chat(self, prompt):
        self.chat_history += [{
            "role": "user",
            "content": prompt,
        }]

        response = self.client.chat.completions.create(
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
    
class Team:
    def __init__(self, client, model, agents):
        self.agents_map = {}
        for agent in agents:
            self.agents_map[agent.name] = agent
        agent_names = [agent.name for agent in agents]
        self.model = model
        self.manager = Agent(
            name='manager',
            client=client, 
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
                "name": "",
            }}
            """)

    def start(self, problem):
        prev_agent = None
        while True:
            if prev_agent:
                eligible_agents = [agent.name for agent in self.agents_map.values() if agent.name != prev_agent],
                self.update_system_message(eligible_agents)

            response = self.manager.chat(f"Which agent shoud respond to this? {problem} Respond in this format: {{\"name\": \"\"}}")

            next_agent = json.loads(response)["name"]

            if next_agent in self.agents_map:
                problem = self.agents_map[next_agent].chat(problem)

            prev_agent = next_agent
            
