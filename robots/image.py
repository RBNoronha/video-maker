import json
import os
import requests
from googleapiclient.discovery import build

def fetch_images_of_all_sentences(content):
    for sentence in content["sentences"]:
        query = f"{content['searchTerm']} {sentence['keywords'][0]}"
        sentence["images"] = fetch_google_and_return_images_links(query)
        sentence["googleSearchQuery"] = query

def fetch_google_and_return_images_links(query):
    api_key = load_google_search_credentials()["apiKey"]
    search_engine_id = load_google_search_credentials()["searchEngineId"]
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=search_engine_id, searchType="image", num=2).execute()
    return [item["link"] for item in res["items"]]

def download_all_images(content):
    content["downloadedImages"] = []
    for sentence in content["sentences"]:
        for image_url in sentence["images"]:
            if image_url not in content["downloadedImages"]:
                download_and_save(image_url, f"{sentence['index']}-original.png")
                content["downloadedImages"].append(image_url)
                break

def download_and_save(url, file_name):
    response = requests.get(url)
    with open(f"./content/{file_name}", "wb") as file:
        file.write(response.content)

def load_google_search_credentials():
    with open("credentials/google-search.json", "r") as file:
        return json.load(file)

def run():
    content = load_state()
    fetch_images_of_all_sentences(content)
    download_all_images(content)
    save_state(content)

def save_state(content):
    with open("state.json", "w") as file:
        json.dump(content, file)

def load_state():
    with open("state.json", "r") as file:
        return json.load(file)

if __name__ == "__main__":
    run()
