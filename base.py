import inspect
import json
from typing import get_type_hints
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Agent:
    def __init__(self, name, model, system_message="", tools=[]):
        self.chat_history = [
            {
                "role": "system",
                "content": system_message
            }
        ]
        self.name = name
        self.model = model
        self.llm = OpenAI(
            base_url=os.getenv("BASE_URL"),
        )
        self.tools = {}
        for tool in tools:
            self.tools[tool.__name__] = tool

    def get_last_message(self):
        return self.chat_history[-1]["content"]

    def chat(self, prompt):
        self.chat_history.append({
            "role": "user",
            "content": prompt,
        })
        
        response = self.llm.chat.completions.create(
            temperature=0,
            messages=self.chat_history,
            model=self.model,
            tools=self._tools_for_api() if len(self.tools) > 0 else None,
            tool_choice="auto" if len(self.tools) > 0 else None,
        )

        response_message = response.choices[0].message
 
        if response_message.tool_calls:
            return self._handle_tool_call(response_message.tool_calls)

        self.chat_history.append({
            "role": "assistant",
            "content": response_message.content,
        }) 

        print(f"🤖 {self.name}:", response_message.content)

        return response_message.content

    def _describe_function(self, func):
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        function_description = {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": inspect.getdoc(func),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }
        
        for name, param in sig.parameters.items():
            param_type = type_hints.get(name, str(param.annotation))
            description = param.annotation.__metadata__[0] if hasattr(param.annotation, '__metadata__') else "No description available"
    
            if param_type == int:
                param_type = "integer"
            elif param_type == float:
                param_type = "number"
            elif param_type == str:
                param_type = "string"
            elif param_type == bool:
                param_type = "boolean"
            elif param_type == list:
                param_type = "array"
            elif param_type == dict:
                param_type = "object"
            
            function_description["function"]["parameters"]["properties"][name] = {
                "type": param_type, 
                "description": description,
            }
            if param.default is inspect.Parameter.empty:
                function_description["function"]["parameters"]["required"].append(name)
        
        return function_description
    
    def _tools_for_api(self):
        return [self._describe_function(tool) for tool in self.tools.values()]

    def _handle_tool_call(self, tool_calls):
        self.chat_history.append({
            "role": "assistant",
            "content": None,
            "tool_calls": tool_calls
        })

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = self.tools[function_name]
            function_args = json.loads(tool_call.function.arguments)
            print(f"🤖 {self.name} calling function", function_name)
            print(f"🤖 {self.name} arguments:", function_args)
            function_response = function_to_call(**function_args)
            print("🛠️ response:", function_response)
            self.chat_history.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),
                }
            )

        call_result_response = self.llm.chat.completions.create(
            temperature=0,
            messages=self.chat_history,
            model=self.model,
        )

        if call_result_response.choices[0].message.content:
            print(f"🤖 {self.name}:", call_result_response.choices[0].message.content)
            self.chat_history.append({
                "role": "assistant",
                "content": call_result_response.choices[0].message.content,
            })

            return call_result_response.choices[0].message.content

        return None

    def update_system_message(self, new_system_message):
        self.chat_history[0] = {
            "role": "system",
            "content": new_system_message
        }

    def reset(self):
        self.chat_history = self.chat_history[:1]
    
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
