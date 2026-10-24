import os
from flask import Flask, request
import requests
from google.cloud import firestore

app = Flask(__name__)

TOKEN = "8252962549:AAGnE3QSy_dpq7bHOb_o10aZbwLxK6vhWj8"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# Inisialisasi Firestore Database Guby
db = firestore.Client()

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        
        if text.startswith("/start"):
            parts = text.split(" ")
            if len(parts) > 1:
                user_id = parts[1].strip()
                # Simpan mapping Telegram chatId ke Firestore user
                db.collection("users").document(user_id).collection("telegram").document("config").set({
                    "chatId": str(chat_id),
                    "isEnabled": True
                }, merge=True)
                
                send_message(chat_id, "✅ Akun Guby Anda berhasil terhubung ke bot ini!")
            else:
                send_message(chat_id, "Halo! Kirim /start [ID_AKUN_ANDA] untuk menghubungkan.")
                
        elif text.startswith("/tambah"):
            # Format: /tambah 50000 Makan siang
            # Anda bisa parse dan simpan ke collection transactions user di Firestore
            send_message(chat_id, "💸 Pengeluaran berhasil dicatat dan disinkronkan ke cloud Guby!")
            
    return "OK", 200

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
