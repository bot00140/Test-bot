import os
from flask import Flask, request
import telebot

# 1. Initialize the Telegram Bot using python-telegram-bot
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# 2. Setup Flask (Render needs a web server to stay alive)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # Replace 'your-app-name.onrender.com' dynamically using environment vars later
    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
    bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
    return "Bot is running!", 200

# 3. Simple Bot Handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am alive and hosted entirely from a phone!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"You said: {message.text}")

if __name__ == "__main__":
    # Render binds to port 10000 by default or via environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
