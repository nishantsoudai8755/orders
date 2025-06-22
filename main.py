from flask import Flask, request
import datetime
import json

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
    app.run()
