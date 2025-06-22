from flask import Flask, request
import datetime
import json
import os  # ✅ ye line missing thi

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Webhook server running!"

@app.route('/order', methods=['POST'])
def order_created():
    data = request.json
    print("📦 New Order:", json.dumps(data, indent=2))
    with open("orders.json", "a") as f:
        json.dump(data, f)
        f.write("\n")
    return "✅ Order received", 200

@app.route('/fulfillment', methods=['POST'])
def fulfillment_created():
    data = request.json
    print("🚚 Fulfillment:", json.dumps(data, indent=2))
    with open("fulfillments.json", "a") as f:
        json.dump(data, f)
        f.write("\n")
    return "✅ Fulfillment received", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT env variable
    app.run(host='0.0.0.0', port=port)
