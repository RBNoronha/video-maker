import json
import os

def ask_and_return_search_term():
    return input("Type a Wikipedia search term: ")

def ask_and_return_prefix():
    prefixes = ["Who is", "What is", "The history of"]
    print("Choose one option:")
    for i, prefix in enumerate(prefixes):
        print(f"{i + 1}. {prefix}")
    selected_prefix_index = int(input()) - 1
    return prefixes[selected_prefix_index]

def save_state(content):
    with open("state.json", "w") as file:
        json.dump(content, file)

def run():
    content = {"maximumSentences": 7}
    content["searchTerm"] = ask_and_return_search_term()
    content["prefix"] = ask_and_return_prefix()
    save_state(content)

if __name__ == "__main__":
    run()
