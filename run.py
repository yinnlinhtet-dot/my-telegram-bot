import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# User data သိမ်းဆည်းရန်
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ! Bot အလုပ်လုပ်နေပါပြီ။ ကျေးဇူးပြု၍ /key ဖြင့် Key စစ်ဆေးပါ။")

async def key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    user_data[chat_id] = {"authenticated": True}
    await update.message.reply_text("Key အတည်ပြုပြီးပါပြီ။ ယခု /input နှင့်အတူ URL ကို ဆက်ပို့နိုင်ပါပြီ။")

async def input_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    if chat_id not in user_data or not user_data[chat_id].get("authenticated"):
        await update.message.reply_text("ကျေးဇူးပြု၍ ပထမဦးစွာ /key ဖြင့် Key အရင်စစ်ဆေးပါ။")
        return
    
    text = update.message.text
    await update.message.reply_text(f"URL ကို အောင်မြင်စွာ လက်ခံရရှိပါပြီရှင်။")

if __name__ == '__main__':
    Thread(target=run_flask).start()
    TOKEN = os.environ.get('BOT_TOKEN')
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("key", key_command))
    application.add_handler(CommandHandler("input", input_command))
    
    application.run_polling()
