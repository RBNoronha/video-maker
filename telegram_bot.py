import telepot
from telepot.loop import MessageLoop
import main

def handle_message(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    if command == '/start':
        bot.sendMessage(chat_id, "Welcome to the Video Maker Bot! Send me a topic to create a video.")
    else:
        main.run_video_maker(command)
        bot.sendMessage(chat_id, "Your video has been created and uploaded to YouTube!")

bot = telepot.Bot('YOUR_TELEGRAM_BOT_API_KEY')
MessageLoop(bot, handle_message).run_as_thread()

print('Listening for incoming messages...')
