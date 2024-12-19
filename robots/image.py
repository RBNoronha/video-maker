import json
import os
import requests
from googleapiclient.discovery import build

def fetch_images_of_all_sentences(content):
    image_source = content.get("image_source", "google")
    for sentence in content["sentences"]:
        query = f"{content['searchTerm']} {sentence['keywords'][0]}"
        if image_source == "google":
            sentence["images"] = fetch_google_and_return_images_links(query)
        elif image_source == "bing":
            sentence["images"] = fetch_bing_and_return_images_links(query)
        else:
            sentence["images"] = fetch_google_and_return_images_links(query)
        sentence["googleSearchQuery"] = query

def fetch_google_and_return_images_links(query):
    api_key = load_google_search_credentials()["apiKey"]
    search_engine_id = load_google_search_credentials()["searchEngineId"]
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=search_engine_id, searchType="image", num=2).execute()
    return [item["link"] for item in res["items"]]

def fetch_bing_and_return_images_links(query):
    api_key = load_bing_search_credentials()["apiKey"]
    search_url = f"https://api.bing.microsoft.com/v7.0/images/search?q={query}&count=2"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    response = requests.get(search_url, headers=headers)
    data = response.json()
    return [item["contentUrl"] for item in data["value"]]

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

def load_bing_search_credentials():
    with open("credentials/bing-search.json", "r") as file:
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
