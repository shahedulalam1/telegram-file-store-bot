import os
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

if not BOT_TOKEN or not CHANNEL_ID:
    raise SystemExit("❌ BOT_TOKEN এবং CHANNEL_ID এনভায়রনমেন্ট ভ্যারিয়েবল সেট করো।")

# শুধু এই আইডিগুলো ফাইল আপলোড করতে পারবে (কমা দিয়ে একাধিক আইডি দেওয়া যায়)
OWNER_IDS = {
    int(x.strip())
    for x in os.getenv("OWNER_ID", "").split(",")
    if x.strip().isdigit()
}
if not OWNER_IDS:
    print("⚠️ OWNER_ID সেট করা নেই, তাই কেউই ফাইল আপলোড করতে পারবে না। লিংক খোলা কাজ করবে।")

bot = telebot.TeleBot(BOT_TOKEN)
BOT_USERNAME = bot.get_me().username  # একবারই নেওয়া হয়

app_flask = Flask(__name__)


def is_owner(message):
    return message.from_user is not None and message.from_user.id in OWNER_IDS


@app_flask.route('/')
def home():
    return "Bot is running!"


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)


@bot.message_handler(commands=['start'])
def handle_start(message):
    parts = message.text.split()
    if len(parts) > 1 and parts[1].startswith("file_"):
        file_key = parts[1][len("file_"):]
        # file_key মানেই চ্যানেলের message_id, তাই আলাদা DB লাগে না
        if file_key.isdigit():
            try:
                bot.copy_message(message.chat.id, CHANNEL_ID, int(file_key))
                return
            except Exception as e:
                print("copy error:", e)
        bot.reply_to(message, "❌ ফাইল পাওয়া যায়নি।")
        return
    if is_owner(message):
        bot.reply_to(
            message,
            "♾️ আনলিমিটেড ফাইল স্টোর বটে স্বাগতম\n\n"
            "আমাকে যেকোনো ফাইল পাঠাও, আমি পার্মানেন্ট লিংক বানিয়ে দেব।"
        )
    else:
        bot.reply_to(message, "🔒 এই বটে শুধু মালিক ফাইল আপলোড করতে পারেন।")


@bot.message_handler(content_types=[
    'document', 'photo', 'video', 'audio', 'voice',
    'sticker', 'animation', 'video_note'
])
def handle_file(message):
    if not is_owner(message):
        return  # মালিক ছাড়া অন্য কারও আপলোড নেওয়া হয় না, কোনো সাড়াও দেওয়া হয় না
    try:
        sent = bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
        share_link = f"https://t.me/{BOT_USERNAME}?start=file_{sent.message_id}"
        bot.reply_to(message, f"✅ সেভ হয়েছে!\n\n🔗 শেয়ার লিংক:\n{share_link}")
    except Exception as e:
        bot.reply_to(message, f"❌ এরর হয়েছে: {e}\nচ্যানেলে বট Admin আছে কিনা চেক করো।")


if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot Running...")
    bot.infinity_polling(skip_pending=True)
