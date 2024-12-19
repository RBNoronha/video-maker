import json

content_file_path = './content.json'

def save(content):
    with open(content_file_path, 'w') as content_file:
        json.dump(content, content_file)

def load():
    with open(content_file_path, 'r') as content_file:
        return json.load(content_file)

content = load()
content['videoDuration'] = 5  # Default duration if not specified
save(content)
