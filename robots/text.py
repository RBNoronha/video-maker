import json
import os
import requests
import feedparser

def fetch_content_from_wikipedia(search_term):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search_term}"
    response = requests.get(url)
    data = response.json()
    return data["extract"]

def fetch_content_from_rss(feed_url, news_index):
    feed = feedparser.parse(feed_url)
    news_item = feed.entries[news_index]
    return news_item.description

def sanitize_content(content):
    without_blank_lines_and_markdown = remove_blank_lines_and_markdown(content)
    without_dates_in_parentheses = remove_dates_in_parentheses(without_blank_lines_and_markdown)
    return without_dates_in_parentheses

def remove_blank_lines_and_markdown(text):
    all_lines = text.split("\n")
    without_blank_lines_and_markdown = [line for line in all_lines if line.strip() and not line.strip().startswith("=")]
    return " ".join(without_blank_lines_and_markdown)

def remove_dates_in_parentheses(text):
    return text.replace(r"\((?:\([^()]*\)|[^()])*\)", "").replace("  ", " ")

def break_content_into_sentences(content):
    sentences = content.split(". ")
    return [{"text": sentence, "keywords": [], "images": []} for sentence in sentences]

def limit_maximum_sentences(sentences, maximum_sentences):
    return sentences[:maximum_sentences]

def fetch_keywords_of_all_sentences(sentences, api_key, endpoint):
    for sentence in sentences:
        sentence["keywords"] = fetch_keywords(sentence["text"], api_key, endpoint)
    return sentences

def fetch_keywords(text, api_key, endpoint):
    url = f"{endpoint}/text/analytics/v3.0/keyPhrases"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    documents = {"documents": [{"id": "1", "language": "en", "text": text}]}
    response = requests.post(url, headers=headers, json=documents)
    data = response.json()
    return data["documents"][0]["keyPhrases"]

def save_state(content):
    with open("state.json", "w") as file:
        json.dump(content, file)

def load_state():
    with open("state.json", "r") as file:
        return json.load(file)

def run():
    content = load_state()
    if "rssFeedUrl" in content and "newsIndex" in content:
        content["sourceContentOriginal"] = fetch_content_from_rss(content["rssFeedUrl"], content["newsIndex"])
    else:
        content["sourceContentOriginal"] = fetch_content_from_wikipedia(content["searchTerm"])
    content["sourceContentSanitized"] = sanitize_content(content["sourceContentOriginal"])
    content["sentences"] = break_content_into_sentences(content["sourceContentSanitized"])
    content["sentences"] = limit_maximum_sentences(content["sentences"], content["maximumSentences"])
    credentials = load_azure_credentials()
    content["sentences"] = fetch_keywords_of_all_sentences(content["sentences"], credentials["apiKey"], credentials["endpoint"])
    save_state(content)

def load_azure_credentials():
    with open("credentials/azure-text-analytics.json", "r") as file:
        return json.load(file)

if __name__ == "__main__":
    run()
