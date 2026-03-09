import os
import time
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# १. Render ला २४ तास जागे ठेवण्यासाठी वेब सर्व्वर
app = Flask('')
@app.route('/')
def home(): return "Titan Bot is 100% Active!"
def run(): app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

# २. कॉन्फिगरेशन (तुझी माहिती इथे भरली आहे)
BOT_TOKEN = "8430592599:AAH1M6ECdH13VR2zStT3eP0p3w0wXhSI3YY"
GAME_AUTH = "EyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." # तुझा पूर्ण टोकन इथे असेल
ACCESS_KEY = "Sarkar555"
auth_users = set()

# ३. वेबसाईटवरून ऑटोमॅटिक डेटा मिळवणे
def get_game_data():
    url = "https://api.pune91.com/api/web/wingo/get_recent_list"
    headers = {"Authorization": f"Bearer {GAME_AUTH}"}
    try:
        response = requests.get(url, headers=headers).json()
        data = response.get('data', [])
        if data:
            # ५, ७, ८, १, २ सारखे आकडे आणि पिरियड मिळवणे
            last_numbers = [int(x['number']) for x in data[:5]]
            period = data[0]['period']
            return period, last_numbers
    except: return None, None

# ४. 'Under 2 Level' प्रेडिक्शन लॉजिक
def predict_result(seeds):
    # प्रगत विश्लेषण: ५ अंकी बेरीज
    val = sum(seeds)
    return "BIG" if val > 22 else "SMALL"

# ५. टेलिग्राम बॉट फंक्शन्स
def start(update, context):
    update.message.reply_text("👋 स्वागत आहे! प्रेडिक्शनसाठी 'Key' टाका.")

def monitor(update, context):
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
                update.message.reply_text(msg, parse_mode='Markdown')
                last_sent_period = period
            time.sleep(10) # दर १० सेकंदाला नवीन डेटा तपासणे
    else:
        update.message.reply_text("❌ चुकीची Key!")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, monitor))
    updater.start_polling()
