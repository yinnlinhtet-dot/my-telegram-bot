import os
import telebot
from flask import Flask
from threading import Thread

# Environment variable ထဲက BOT_TOKEN ကို ယူခြင်း
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is active!")

if __name__ == '__main__':
    # Flask ဆာဗာကို Background မှာ Run ခြင်း
    Thread(target=run_flask).start()
    
    # Telegram Bot ကို စတင် Run ခြင်း
    bot.infinity_polling()
