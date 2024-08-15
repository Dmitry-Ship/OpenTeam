import json
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv(override=True)

class Agent:
    def __init__(self, name, model, system_message="", tools_params=[], tools_mapper={}):
        self.chat_history = [{
            "role": "system",
            "content": system_message
        }]
        
        self.name = name
        self.model = model
        self.llm = OpenAI(
            base_url=os.getenv("BASE_URL"),
        )
        self.tools_params = tools_params
        self.tools_mapper = tools_mapper

    def chat(self, prompt):
        self.chat_history.append({
            "role": "user",
            "content": prompt,
        })
        
        response = self.llm.chat.completions.create(
            temperature=0,
            messages=self.chat_history,
            model=self.model,
            tools=self.tools_params if len(self.tools_params) > 0 else None,
            tool_choice="auto" if len(self.tools_params) > 0 else None,
        )

        response_message = response.choices[0].message
 
        if response_message.tool_calls:
            response_message = self.handle_tool_calls(response_message.tool_calls)

        self.chat_history.append({
            "role": "assistant",
            "content": response_message.content,
        }) 

        print(f"🤖 {self.name}:", response_message.content)

        return response_message.content

    def handle_tool_calls(self, tool_calls: list):
        self.chat_history.append({
            "role": "assistant",
            "content": None,
            "tool_calls": tool_calls
        })

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            print(f"🤖 {self.name} calling function", function_name)
            print(f"🤖 {self.name} arguments:", function_args)
            function_response = self.tools_mapper[function_name](**function_args)
            print("🛠️ response:", function_response)
            self.chat_history.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response),
            })

        resp = self.llm.chat.completions.create(
                temperature=0,
                messages=self.chat_history,
                model=self.model,
            )

        response_message = resp.choices[0].message
        return response_message

  
        
    
