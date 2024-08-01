import json
import inquirer
from .agents import search_query_suggester, searcher

selected_suggestion = None
while True:
    if selected_suggestion is None:
        query = input("search 🔍: ")
    else:
        query = selected_suggestion
    
    search_result = searcher.chat(query)


    suggestions_result = search_query_suggester.chat(search_result)
    data = json.loads(suggestions_result)
    suggestions = data['related']

    choice = inquirer.prompt([
        inquirer.List(
            'choice',
            message="Here are some suggestions:",
            choices=suggestions + ["other"],
            carousel=True
        )
    ])

    query = choice['choice']
    if query == 'other':
        selected_suggestion = None
        continue

    selected_suggestion = query




