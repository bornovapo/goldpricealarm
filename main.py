import time
import requests
import websocket
import json

# Kendi bilgilerini buraya yaz
TELEGRAM_TOKEN = "9263578922:AAHlhaRzMq-cS-XTHxha2uWqmbVH83qD4sg
"
CHAT_ID = "1411420528"

# Binance Futures XAU (Gold) WebSocket adresi
WS_URL = "wss://fstream.binance.com/ws/paxgusdt@ticker"

last_price = None

def send_telegram_alert(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Bildirim hatasi: {e}")

def on_message(ws, message):
    global last_price
    try:
        data = json.loads(message)
        current_price = float(data['c']) # Güncel fiyat
        
        if last_price is not None:
            drop = last_price - current_price
            # Örnek koşul: Anlık 2 dolardan fazla düşüş olursa bildir
            if drop >= 2.0:
                alert_text = f"🚨 **XAUUSD SERT DÜŞÜŞ!**\n\nFiyat: `{current_price}`\nDüşüş Miktarı: `-${drop:.2f}`"
                send_telegram_alert(alert_text)
                last_price = current_price
                
        last_price = current_price
    except Exception as e:
        print(f"Hata: {e}")

def on_error(ws, error):
    print(f"Baglanti hatasi: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Baglanti kapandi, yeniden baglaniliyor...")
    time.sleep(5)
    run_bot()

def on_open(ws):
    print("Binance canlı XAU akışına bağlandı.")

def run_bot():
    ws = websocket.WebSocketApp(WS_URL,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    run_bot()
