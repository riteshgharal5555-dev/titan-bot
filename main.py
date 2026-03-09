import os
import time
import requests
from flask import Flask
from threading import Thread

# १. Render ला २४ तास जागे ठेवण्यासाठी वेब सर्व्हर
app = Flask('')
@app.route('/')
def home(): return "Titan Bot is 100% Active!"

def run(): app.run(host='0.0.0.0', port=8080)

def start_logic():
    # इथे आपण तुझा टोकन वापरून ५, ७, ८, १, २ आकडे आपोआप वाचू
    while True:
        try:
            print("Analyzing Live Seed Data...")
            # तुझा 'Hard Analysis' कोड इथे कार्य करेल
            time.sleep(30)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    start_logic()
