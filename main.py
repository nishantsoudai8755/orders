from flask import Flask, request
import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Webhook server running!"

@app.route('/order', methods=['POST'])
def order_created():
    data = request.json
    print("📦 New Order:", json.dumps(data, indent=2))

    # Format the filename based on timestamp
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"orders/order-{now}.json"

    os.makedirs("orders", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    return "✅ Order saved to GitHub repo", 200

@app.route('/fulfillment', methods=['POST'])
def fulfillment_created():
    data = request.json
    print("🚚 Fulfillment:", json.dumps(data, indent=2))

    # Format the filename based on timestamp
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"fulfillments/fulfillment-{now}.json"

    os.makedirs("fulfillments", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    return "✅ Fulfillment saved to GitHub repo", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
