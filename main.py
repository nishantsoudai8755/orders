from flask import Flask, request
import datetime
import json
import os
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Webhook server running!"

@app.route('/order', methods=['POST'])
def order_created():
    data = request.json
    print("📦 New Order:", json.dumps(data, indent=2))

    # Extract relevant data
    shipping = data.get("shipping_address", {})
    name = shipping.get("name", "")
    phone = shipping.get("phone", "")
    address = shipping.get("address1", "")
    city = shipping.get("city", "")
    state = shipping.get("province", "")
    country = shipping.get("country", "")
    zip_code = shipping.get("zip", "")
    amount = data.get("total_price", "")

    # File path for orders.csv
    file_path = "orders.csv"

    # Write to CSV
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Phone", "Address", "City", "State", "Country", "Zip", "Amount", "Date"])
        writer.writerow([name, phone, address, city, state, country, zip_code, amount, datetime.datetime.now().isoformat()])

    return "✅ Order saved to CSV", 200

@app.route('/fulfillment', methods=['POST'])
def fulfillment_created():
    data = request.json
    print("🚚 Fulfillment:", json.dumps(data, indent=2))
    with open("fulfillments.json", "a") as f:
        json.dump(data, f)
        f.write("\n")
    return "✅ Fulfillment received", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
