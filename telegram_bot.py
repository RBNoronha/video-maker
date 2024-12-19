import telepot
from telepot.loop import MessageLoop
import main
import schedule
import time

def handle_message(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    if command == '/start':
        bot.sendMessage(chat_id, "Welcome to the Video Maker Bot! Send me a topic to create a video.")
    elif command == '/help':
        bot.sendMessage(chat_id, "Available commands:\n/start - Start the bot\n/help - Display this help message\n/status - Check the status of the video creation process\n/cancel - Cancel the current video creation process\n/schedule - Schedule a video creation task\n/customize - Customize video creation options")
    elif command == '/status':
        bot.sendMessage(chat_id, "The video creation process is currently in progress.")
    elif command == '/cancel':
        bot.sendMessage(chat_id, "The video creation process has been canceled.")
    elif command.startswith('/schedule'):
        schedule_time = command.split(' ')[1]
        schedule.every().day.at(schedule_time).do(main.run_video_maker, command.split(' ')[2])
        bot.sendMessage(chat_id, f"Video creation task scheduled at {schedule_time}.")
    elif command.startswith('/customize'):
        options = command.split(' ')[1:]
        main.run_video_maker_with_options(options)
        bot.sendMessage(chat_id, "Your video has been created with the customized options and uploaded to YouTube!")
    else:
        main.run_video_maker(command)
        bot.sendMessage(chat_id, "Your video has been created and uploaded to YouTube!")

bot = telepot.Bot('YOUR_TELEGRAM_BOT_API_KEY')
MessageLoop(bot, handle_message).run_as_thread()

print('Listening for incoming messages...')

while True:
    schedule.run_pending()
    time.sleep(1)
