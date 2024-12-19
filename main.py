import robots.input as input_robot
import robots.text as text_robot
import robots.image as image_robot
import robots.video as video_robot
import robots.youtube as youtube_robot
import telegram_bot  # Import the telegram_bot.py file

def main():
    input_robot.run()
    text_robot.run()
    image_robot.run()
    video_robot.run()
    youtube_robot.run()
    telegram_bot  # Run the Telegram bot

def run_video_maker_with_options(options):
    input_robot.run()
    text_robot.run()
    image_robot.run()
    video_robot.run(options)
    youtube_robot.run()

if __name__ == "__main__":
    main()
