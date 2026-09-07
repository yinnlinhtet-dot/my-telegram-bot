import telebot, asyncio, aiohttp, json, base64, random, re, os, string, time
from telebot.async_telebot import AsyncTeleBot
from aiohttp import web
import cv2
import ddddocr
import numpy as np
from datetime import datetime, timedelta, timezone

# Bot Token နှင့် သင့်ရဲ့ Admin ID အသစ်ကို ထည့်သွင်းရန်
BOT_TOKEN = '8628864483:AAEtdYTyv3ducRn'
GITHUB_TOKEN = 'ghp_SznMfaU45MnKdh6ApjN'
ADMIN_ID = "8991689638"
REPO_OWNER = "yinnlinhtet-dot"
REPO_NAME = "my-telegram-bot"
#####################

SUCCESS_CODE = asyncio.Queue()
bot = AsyncTeleBot(BOT_TOKEN)
user_data = {}
approve = {}
scan_tasks = {}
success_messages = {}
success_texts = {}
limited_messages = {}
limited_texts = {}
captcha_state = {}
session = None
_connector = None
CONCURRENCY = 3000
_voucher_sem = None
_start_time = time.monotonic()

async def handle(request):
    return web.Response(text="Bot is awake and running 24/7!")

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8099))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def get_file_content(path):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            content = base64.b64decode(data['content']).decode('utf-8')
            return json.loads(content), data['sha']
    return None, None

async def update_file_content(path, content, sha, message):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    encoded = base64.b64encode(json.dumps(content).encode()).decode()
    payload = {
        "message": message,
        "content": encoded,
        "sha": sha
    }
    async with session.put(url, headers=headers, json=payload) as response:
        return await response.text()

@bot.message_handler(commands=['start'])
async def start(message):
    await bot.reply_to(message, "Bot စတင်ပြီ။ /key ဖြင့်စတင်ပါ")

@bot.message_handler(commands=['key'])
async def handle_key(message):
    global approve
    key = str(message.chat.id)
    auth_list, _ = await get_file_content('auth_list.json')
    if key in auth_list:
        valid = check_key_expiration(auth_list[key])
        if valid:
            approve[message.chat.id] = True
            user_data[message.chat.id] = {}
            await bot.reply_to(
                message,
                "Key မှန်ကန်ပါသည် /input ဖြင့် Session URL ထည့်ပါ"
            )
        else:
            approve[message.chat.id] = False
            await bot.reply_to(
                message,
                "Key Expired ဖြစ်သွားပါပြီ"
            )
    else:
        await bot.reply_to(
            message,
            "သင်၏ key ကို registered မလုပ်ရသေးပါ။"
        )
