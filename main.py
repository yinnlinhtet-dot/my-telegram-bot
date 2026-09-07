import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is active!")

if __name__ == '__main__':
    # Flask ဆာဗာကို Background မှာ Run ရန်
    Thread(target=run_flask).start()
    
    # Environment variable ထဲက BOT_TOKEN ကို ဖတ်ယူခြင်း
    TOKEN = os.environ.get("BOT_TOKEN")
    
    # Telegram Bot Application ကို တည်ဆောက်ခြင်း
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Start command ထည့်သွင်းခြင်း
    application.add_handler(CommandHandler("start", start))
    
    # Bot ကို စတင် Run ခြင်း
    application.run_polling()
