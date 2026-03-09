import sys
# imghdr एरर फिक्स करण्यासाठी ही जादूची ट्रिक
try:
    import imghdr
except ImportError:
    import types
    sys.modules['imghdr'] = types.ModuleType('imghdr')
    sys.modules['imghdr'].what = lambda x, h=None: None

import os
import time
import requests
from flask import Flask
from threading import Thread
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# १. सर्व्हर सेटअप
app = Flask('')
@app.route('/')
def home(): return "Titan Bot is 100% Active!"
def run(): app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

# २. टोकन्स (हे अपडेट ठेवा)
BOT_TOKEN = "8430592599:AAH1M6ECdH13VR2zStT3eP0p3w0wXhSI3YY"
GAME_AUTH = "तुझा_नवीन_टोकन_इथे_टाक" # मघाशी सांगितल्याप्रमाणे नवीन टोकन मिळवून इथे पेस्ट कर
ACCESS_KEY = "Sarkar555"
auth_users = set()

# ३. डेटा फेचिंग
def get_game_data():
    url = "https://api.pune91.com/api/web/wingo/get_recent_list"
    headers = {"Authorization": f"Bearer {GAME_AUTH}"}
    try:
        response = requests.get(url, headers=headers).json()
        data = response.get('data', [])
        if data:
            last_numbers = [int(x['number']) for x in data[:5]]
            period = data[0]['period']
            return period, last_numbers
    except: return None, None

def predict_result(seeds):
    val = sum(seeds)
    return "BIG" if val > 22 else "SMALL"

# ४. टेलिग्राम हँडलर्स
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 स्वागत आहे! प्रेडिक्शनसाठी 'Key' टाका.")

def monitor(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if update.message.text == ACCESS_KEY:
        auth_users.add(user_id)
        update.message.reply_text("✅ Access Granted! आता तुला ऑटोमॅटिक प्रेडिक्शन मिळतील.")
        last_sent_period = ""
        while user_id in auth_users:
            period, seeds = get_game_data()
            if period and period != last_sent_period:
                result = predict_result(seeds)
                msg = f"🎰 *Wingo 1-Min*\nPeriod: `{period}`\nResult: *{result}*\nLevel: *L1 (₹10)*\n[Under 2 Level Fix Win]"
                update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
                last_sent_period = period
            time.sleep(10)
    else:
        update.message.reply_text("❌ चुकीची Key!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, monitor))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    main()
    return "BIG" if val > 22 else "SMALL"

# ५. टेलिग्राम बॉट फंक्शन्स
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 स्वागत आहे! प्रेडिक्शनसाठी 'Key' टाका.")

def monitor(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if update.message.text == ACCESS_KEY:
        auth_users.add(user_id)
        update.message.reply_text("✅ Access Granted! आता तुला ऑटोमॅटिक प्रेडिक्शन मिळतील.")
        last_sent_period = ""
        while user_id in auth_users:
            period, seeds = get_game_data()
            if period and period != last_sent_period:
                result = predict_result(seeds)
                msg = f"🎰 *Wingo 1-Min*\nPeriod: `{period}`\nResult: *{result}*\nLevel: *L1 (₹10)*\n[Under 2 Level Fix Win]"
                update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
                last_sent_period = period
            time.sleep(10)
    else:
        update.message.reply_text("❌ चुकीची Key!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, monitor))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    main()
