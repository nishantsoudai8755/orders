from flask import Flask, request
import json
import requests
import os

app = Flask(__name__)

# Paste your Google Apps Script Web App URL here
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxwUC_pBu_9blQKE1Y9TFNHpcEBPmJxWcgtGwdjL1VxPt9XtF5J9qdMyTkwbwhMBU5t/exec"

@app.route('/')
def home():
    return "✅ Webhook server running!"

@app.route('/order', methods=['POST'])
def order_created():
    data = request.json
    print("📦 Order webhook received")

    filtered = {
        "name": data.get("shipping_address", {}).get("name"),
        "phone": data.get("shipping_address", {}).get("phone"),
        "address": data.get("shipping_address", {}).get("address1"),
        "city": data.get("shipping_address", {}).get("city"),
        "price": data.get("total_price")
    }

    send_to_sheets("order", filtered)
    return "✅ Order processed", 200

@app.route('/fulfillment', methods=['POST'])
def fulfillment_created():
    data = request.json
    print("🚚 Fulfillment webhook received")

    filtered = {
        "name": data.get("destination", {}).get("name"),
        "phone": data.get("destination", {}).get("phone"),
        "tracking_url": data.get("tracking_url"),
        "product_names": [item.get("name") for item in data.get("line_items", [])]
    }

    send_to_sheets("fulfillment", filtered)
    return "✅ Fulfillment processed", 200

def send_to_sheets(event_type, filtered_data):
    payload = {
        "type": event_type,
        "data": filtered_data
    }
    try:
        res = requests.post(GOOGLE_SCRIPT_URL, json=payload)
        print("📤 Sent to Google Sheets:", res.text)
    except Exception as e:
        print("❌ Failed to send to Sheets:", str(e))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
