import os
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

bot = telebot.TeleBot(BOT_TOKEN)

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

FILE_DB = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    text = message.text.split()
    if len(text) > 1 and text[1].startswith("file_"):
        file_key = text[1].replace("file_", "")
        if file_key in FILE_DB:
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, FILE_DB[file_key])
                return
            except:
                pass
        bot.reply_to(message, "❌ ফাইল পাওয়া যায়নি।")
        return
    bot.reply_to(message, "♾️ আনলিমিটেড ফাইল স্টোর বটে স্বাগতম\n\nআমাকে যেকোনো ফাইল পাঠাও, আমি পার্মানেন্ট লিংক বানিয়ে দেব।")

@bot.message_handler(content_types=['document', 'photo', 'video', 'audio', 'voice', 'sticker'])
def handle_file(message):
    try:
        sent = bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
        file_key = str(sent.message_id)
        FILE_DB[file_key] = sent.message_id
        bot_username = bot.get_me().username
        share_link = f"https://t.me/{bot_username}?start=file_{file_key}"
        bot.reply_to(message, f"✅ সেভ হয়েছে!\n\n🔗 শেয়ার লিংক:\n{share_link}")
    except Exception as e:
        bot.reply_to(message, f"❌ এরর হয়েছে: {e}\nচ্যানেলে বট Admin আছে কিনা চেক করো।")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot Running...")
    bot.infinity_polling(skip_pending=True)