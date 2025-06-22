from flask import Flask, request
import json, os, datetime

app = Flask(__name__)

def save_to_file(folder, prefix, data):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{folder}/{prefix}-{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"📁 Saved: {filename}")

@app.route('/')
def home():
    return "✅ Webhook server is live!"

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    save_to_file("orders", "order", data)
    return "✅ Order received", 200

@app.route('/fulfillment', methods=['POST'])
def fulfillment():
    data = request.json
    save_to_file("fulfillments", "fulfillment", data)
    return "✅ Fulfillment received", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
