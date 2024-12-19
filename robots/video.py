import os
import json
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont

def convert_all_images(content):
    for sentence_index in range(len(content["sentences"])):
        convert_image(sentence_index)

def convert_image(sentence_index):
    input_file = f"./content/{sentence_index}-original.png"
    output_file = f"./content/{sentence_index}-converted.png"
    width, height = 1920, 1080

    image = Image.open(input_file)
    image = image.resize((width, height), Image.ANTIALIAS)
    image.save(output_file)

def create_all_sentence_images(content):
    for sentence_index, sentence in enumerate(content["sentences"]):
        create_sentence_image(sentence_index, sentence["text"], content.get("text_styles", {}))

def create_sentence_image(sentence_index, sentence_text, text_styles):
    output_file = f"./content/{sentence_index}-sentence.png"
    width, height = 1920, 400

    image = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    font_path = text_styles.get("font", "arial.ttf")
    font_size = text_styles.get("size", 40)
    font_color = text_styles.get("color", (255, 255, 255))
    font_position = text_styles.get("position", (10, 10))
    font = ImageFont.truetype(font_path, font_size)
    draw.text(font_position, sentence_text, font=font, fill=font_color)
    image.save(output_file)

def create_youtube_thumbnail():
    input_file = "./content/0-converted.png"
    output_file = "./content/youtube-thumbnail.jpg"

    image = Image.open(input_file)
    image.save(output_file)

def render_video_with_moviepy(content):
    clips = []
    default_duration = content.get("default_duration", 5)
    for sentence_index in range(len(content["sentences"])):
        image_path = f"./content/{sentence_index}-converted.png"
        sentence_image_path = f"./content/{sentence_index}-sentence.png"
        duration = content["sentences"][sentence_index].get("duration", default_duration)
        image_clip = mp.ImageClip(image_path).set_duration(duration)
        sentence_clip = mp.ImageClip(sentence_image_path).set_duration(duration)
        final_clip = mp.CompositeVideoClip([image_clip, sentence_clip.set_position(("center", "bottom"))])
        clips.append(final_clip)

    video = mp.concatenate_videoclips(clips, method="compose")
    video.write_videofile("./content/video.mp4", fps=24)

def run():
    content = load_state()
    convert_all_images(content)
    create_all_sentence_images(content)
    create_youtube_thumbnail()
    render_video_with_moviepy(content)
    save_state(content)

def save_state(content):
    with open("state.json", "w") as file:
        json.dump(content, file)

def load_state():
    with open("state.json", "r") as file:
        return json.load(file)

if __name__ == "__main__":
    run()
