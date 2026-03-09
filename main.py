import os
import time
import requests
from flask import Flask
from threading import Thread
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# १. Render ला २४ तास जागे ठेवण्यासाठी वेब सर्व्हर
app = Flask('')
@app.route('/')
def home(): return "Titan Bot is 100% Active!"
def run(): app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

# २. तुझे कॉन्फिगरेशन
BOT_TOKEN = "8430592599:AAH1M6ECdH13VR2zStT3eP0p3w0wXhSI3YY"
GAME_AUTH = "EyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzczMDQ0MjUyIiwibmJmIjoiMTc3MzA0NDI1MiIsImV4cCI6IjE3NzMwNDYwNTIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIzLzkvMjAyNiAyOjE3OjMyIFBNIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQWNjZXNzX1Rva2VuIiwiVXNlcklkIjoiMzA4MTU1MCIsIlVzZXJOYW1lIjoiOTE4NTkxNjYxODM5IiwiVXNlclBob3RvIjoiNiIsIk5pY2tOYW1lIjoiTWVtYmVyTk5HS0xMVksiLCJBbW91bnQiOiIyMDUuMDciLCJJbnRlZ3JhbCI6IjAiLCJMb2dpbk1hcmsiOiJINSIsIkxvZ2luVGltZSI6IjMvOS8yMDI2IDE6NDc6MzIgUE0iLCJMb2dpbklQQWRkcmVzcyI6IjI0MDk6NDBjMjo1NDIwOjFlNjQ6NjU1MDo0MWJhOjJkYWI6NWQ0NiIsIkRiTnVtYmVyIjoiMCIsIklzdmFsaWRhdG9yIjoiMCIsIktleUNvZGUiOiI2ODEiLCJUb2tlblR5cGUiOiJBY2Nlc3NfVG9rZW4iLCJQaG9uZVR5cGUiOiIxIiwiVXNlclR5cGUiOiIwIiwiVXNlck5hbWUyIjoiIiwiaXNzIjoiand0SXNzdWVyIiwiYXVkIjoibG90dGVyeVRpY2tldCJ9.PH3DWOce4Hv646BJv3lANaLS9ACVoqryD3Yg1z3BJR8"
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
            last_numbers = [int(x['number']) for x in data[:5]]
            period = data[0]['period']
            return period, last_numbers
    except: return None, None

# ४. प्रेडिक्शन लॉजिक (Under 2 Level)
def predict_result(seeds):
    val = sum(seeds)
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
