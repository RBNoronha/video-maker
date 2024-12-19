import telepot
from telepot.loop import MessageLoop
import main
import schedule
import time
import logging
import feedparser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RSS_FEEDS = {
    "Feed 1": "https://example.com/rss1.xml",
    "Feed 2": "https://example.com/rss2.xml",
    "Feed 3": "https://example.com/rss3.xml"
}

def fetch_rss_feed_urls():
    return RSS_FEEDS

def fetch_news_items_from_feed(feed_url):
    feed = feedparser.parse(feed_url)
    news_items = []
    for entry in feed.entries:
        news_items.append({"title": entry.title, "description": entry.description})
    return news_items

def handle_message(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    try:
        if command == '/start':
            bot.sendMessage(chat_id, "Welcome to the Video Maker Bot! Send me a topic to create a video.")
        elif command == '/help':
            bot.sendMessage(chat_id, "Available commands:\n/start - Start the bot\n/help - Display this help message\n/status - Check the status of the video creation process\n/cancel - Cancel the current video creation process\n/schedule - Schedule a video creation task\n/customize - Customize video creation options\n/rss - List available RSS feeds")
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
        elif command == '/rss':
            rss_feeds = fetch_rss_feed_urls()
            keyboard = [[{"text": name, "callback_data": url}] for name, url in rss_feeds.items()]
            reply_markup = {"inline_keyboard": keyboard}
            bot.sendMessage(chat_id, "Select an RSS feed:", reply_markup=reply_markup)
        elif command.startswith('/news'):
            feed_url = command.split(' ')[1]
            news_items = fetch_news_items_from_feed(feed_url)
            news_list = "\n".join([f"{i+1}. {item['title']}" for i, item in enumerate(news_items)])
            bot.sendMessage(chat_id, f"News items:\n{news_list}\n\nSelect a news item by number:")
        elif command.isdigit():
            news_index = int(command) - 1
            feed_url = command.split(' ')[1]
            news_items = fetch_news_items_from_feed(feed_url)
            selected_news = news_items[news_index]
            main.run_video_maker(selected_news['description'])
            bot.sendMessage(chat_id, "Your video has been created and uploaded to YouTube!")
        else:
            main.run_video_maker(command)
            bot.sendMessage(chat_id, "Your video has been created and uploaded to YouTube!")
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        bot.sendMessage(chat_id, "An error occurred while processing your request. Please try again later.")

bot = telepot.Bot('YOUR_TELEGRAM_BOT_API_KEY')
MessageLoop(bot, handle_message).run_as_thread()

logging.info('Listening for incoming messages...')

while True:
    schedule.run_pending()
    time.sleep(1)
