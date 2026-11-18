import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

FILE_DB = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) > 0 and context.args[0].startswith("file_"):
        file_key = context.args[0].replace("file_", "")
        if file_key in FILE_DB:
            await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=FILE_DB[file_key]
            )
            return
        await update.message.reply_text("❌ ফাইল পাওয়া যায়নি।")
        return

    await update.message.reply_text(
        "♾️ আনলিমিটেড ফাইল স্টোর বটে স্বাগতম\n\n"
        "আমাকে যেকোনো ফাইল পাঠাও, আমি পার্মানেন্ট লিংক বানিয়ে দেব।"
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sent_msg = await update.message.forward(chat_id=CHANNEL_ID)
    file_key = str(sent_msg.message_id)
    FILE_DB[file_key] = sent_msg.message_id
    bot_username = (await context.bot.get_me()).username
    share_link = f"https://t.me/{bot_username}?start=file_{file_key}"
    await update.message.reply_text(f"✅ সেভ হয়েছে!\n\n🔗 শেয়ার লিংক:\n{share_link}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_file))
    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()