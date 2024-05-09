
import json
import inquirer
import os
from .agents import suggester, mindmap_creator

flip_id = os.getenv("FLIP_ID")

def get_suggestions(flip_id):
    suggester.chat(f"flip_id: '{flip_id}'")
    data = json.loads(suggester.get_last_message())
    return data['suggestions']

while True:
    suggestions = get_suggestions(flip_id=flip_id)
    answers = inquirer.prompt([
        inquirer.List(
            'choice',
            message="Here are some suggestions:",
            choices=suggestions + ["other"],
            carousel=True
        )
    ])
    query = answers['choice']

    if query == 'other':
        query = input("mindmap 🗺️: ")

    mindmap_creator.chat(query)
