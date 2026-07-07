import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)

# Base URL for your game's Web App (Change this to your actual game URL)
WEBAPP_URL = "https://poke-crimsonsky--viralhit77.replit.app/"

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    host_url = request.url_root.replace("http://", "https://")
    bot.set_webhook(url=host_url + TOKEN)
    return "Bot is running perfectly!", 
# Helper function to create an ultra-reliable URL interface button
def make_hybrid_markup(button_text, webapp_path=""):
    markup = InlineKeyboardMarkup()
    
    # Your actual game base URL
    base_url = "https://poke-crimsonsky--viralhit77.replit.app/" 
    
    # Clean the URL and append path
    base_url = base_url.rstrip('/')
    full_url = f"{base_url}/{webapp_path}" if webapp_path else base_url
    
    # Use standard url parameter to ensure it never crashes
    markup.add(InlineKeyboardButton(text=button_text, url=full_url))
    return markup

    
# --- COMMAND HANDLERS ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Pokémon Adventure Bot! Use the commands to hunt, manage your team, or open the Web App.")

@bot.message_handler(commands=['hunt', 'safari', 'league'])
def handle_hunting(message):
    # Safely extracts 'hunt', 'safari', or 'league'
    cmd = message.text.split()[0].replace('/', '').split('@')[0].strip().lower()
    display_name = cmd.capitalize()
    
    bot.send_message(
        message.chat.id, 
        f"🌲 Entering the {display_name} zone...", 
        reply_markup=make_hybrid_markup(f"🎮 Open {display_name} Screen", webapp_path=cmd)
    )
    

@bot.message_handler(commands=['teams'])
def handle_teams(message):
    bot.send_message(
        message.chat.id,
        "📋 **Your Team**\n1. Pikachu (Lv. 25)\n2. Charizard (Lv. 42)\n\nUse the web app to customize your lineup!",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("🔄 Customize Team in Web App", webapp_path="teams")
    )

@bot.message_handler(commands=['dex'])
def handle_dex(message):
    bot.send_message(
        message.chat.id,
        "📕 **Pokédex Status**\nSeen: 150 | Caught: 89\n\nSearch full entries in the web tool:",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("🔍 Open Pokédex Data", webapp_path="dex")
    )

@bot.message_handler(commands=['region'])
def handle_region(message):
    bot.send_message(
        message.chat.id,
        "🗺️ You are currently in the **Kanto Region**.\nChoose your destination:",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("✈️ Travel Map", webapp_path="region")
    )

@bot.message_handler(commands=['bag'])
def handle_bag(message):
    bot.send_message(
        message.chat.id,
        "🎒 **Your Bag Inventory:**\n• Pokéballs x15\n• Potion x3\n• Rare Candy x1",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("🎒 Open Full Backpack", webapp_path="bag")
    )

@bot.message_handler(commands=['store'])
def handle_store(message):
    bot.send_message(
        message.chat.id,
        "🏪 Opening the PokéMart...",
        reply_markup=make_hybrid_markup("🛒 Enter Store", webapp_path="store")
    )

@bot.message_handler(commands=['mons'])
def handle_mons(message):
    bot.send_message(
        message.chat.id,
        "🦅 **Your Pokémon Box:**\nShowing your latest captures. Open the grid view to manage them.",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("📦 Open Pokémon Box", webapp_path="mons")
    )

@bot.message_handler(commands=['friends'])
def handle_friends(message):
    bot.send_message(
        message.chat.id,
        "👥 **Friends List:**\n• Player1 (Online)\n• TrainerRed (Offline)",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("🤝 Social Dashboard", webapp_path="friends")
    )

@bot.message_handler(commands=['mails'])
def handle_mails(message):
    bot.send_message(
        message.chat.id,
        "📬 **Mailbox:**\n📬 You have (1) unread system claim notification!",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("📩 Read Mail", webapp_path="mails")
    )

@bot.message_handler(commands=['transfer'])
def handle_transfer(message):
    bot.send_message(
        message.chat.id,
        "💸 **Pokedollars Transfer**\nSyntax to transfer in chat: `/transfer @username amount`",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("💳 Bank Web Portal", webapp_path="transfer")
    )

@bot.message_handler(commands=['redeem'])
def handle_redeem(message):
    bot.send_message(
        message.chat.id,
        "🎁 **Promo Code Redemption**\nSyntax to redeem in chat: `/redeem CODE`",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("🎟️ Redeem via Web App", webapp_path="redeem")
    )

@bot.message_handler(commands=['Leaderboad', 'leaderboard'])
def handle_leaderboard(message):
    bot.send_message(
        message.chat.id,
        "🏆 **Global Rankings**\n⚔️ Battlebox Top: Ash\n🛡️ League Top: Gary",
        parse_mode="Markdown",
        reply_markup=make_hybrid_markup("📊 View All Leaderboards", webapp_path="leaderboard")
    )

@bot.message_handler(commands=['mod'])
def handle_mod(message):
    bot.send_message(
        message.chat.id,
        "🛡️ Opening Moderator Panel...",
        reply_markup=make_hybrid_markup("⚙️ Open Mod Screen", webapp_path="mod")
    )

# Standard text catcher to make sure the bot doesn't completely ignore plain messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "I didn't recognize that command. Type /help to see available options!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
