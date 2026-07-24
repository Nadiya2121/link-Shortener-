import telebot
import requests
from config import TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "⚡ Welcome to CloudLink Pro Bot!\nSend me any long link, and I will shorten it for you instantly.")

@bot.message_handler(func=lambda message: True)
def shorten_link(message):
    long_url = message.text.strip()
    if long_url.startswith("http://") or long_url.startswith("https://"):
        try:
            # Shorten request
            response = requests.post("http://127.0.0.1:5000/shorten", data={"url": long_url})
            bot.reply_to(message, f"✅ Your Short Link is Ready:\n\n{response.url}")
        except Exception as e:
            bot.reply_to(message, "❌ Server Error! Make sure your main.py is running.")
    else:
        bot.reply_to(message, "⚠️ Please send a valid URL starting with http:// or https://")

if __name__ == "__main__":
    print("🤖 Telegram Bot Engine Running...")
    bot.infinity_polling()
