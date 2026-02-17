from kafka import KafkaConsumer
import json
import requests
from datetime import datetime

# ------------------------------
# Kafka Consumer
# ------------------------------
topic = 'payment_lines'
consumer = KafkaConsumer(
    topic,
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='payment_consumer_group'
)

# ------------------------------
# Power BI Streaming Dataset
# ------------------------------
# Replace these with your Power BI streaming dataset details
workspace_id = "me/list?experience=power-bi"
dataset_id = "2899c1aa-ccd3-4a71-a910-b6aa03ef12f1"
dataset_key = "https://api.powerbi.com/beta/b14d86f1-83ba-4b13-a702-b5c0231b9337/datasets/2899c1aa-ccd3-4a71-a910-b6aa03ef12f1/rows?experience=power-bi&key=mBFKoEL9Qpu3A8c9FvZ2qF2cdNyKEeRs3Igz%2Ffz%2FM2ZFZIHt079YiES%2FLHLmcfO%2BTkZdMWV47%2BGJIOIBUSI%2Bfg%3D%3D"

# REST endpoint for pushing rows
powerbi_url = f"https://api.powerbi.com/beta/b14d86f1-83ba-4b13-a702-b5c0231b9337/datasets/2899c1aa-ccd3-4a71-a910-b6aa03ef12f1/rows?experience=power-bi&key=mBFKoEL9Qpu3A8c9FvZ2qF2cdNyKEeRs3Igz%2Ffz%2FM2ZFZIHt079YiES%2FLHLmcfO%2BTkZdMWV47%2BGJIOIBUSI%2Bfg%3D%3D"

print("Streaming Kafka messages to Power BI...")

for msg in consumer:
    payment = msg.value

    # Ensure bank_amt is numeric and deposit_date is ISO
    bank_amt = float(payment.get("bank_amt", 0))
    deposit_ref = payment.get("deposit_ref", "")
    deposit_date = payment.get("deposit_date")
    if isinstance(deposit_date, str):
        deposit_date_iso = deposit_date
    elif isinstance(deposit_date, datetime):
        deposit_date_iso = deposit_date.isoformat()
    else:
        deposit_date_iso = datetime.now().isoformat()

    # Prepare row for Power BI
    row = {
        "DepositRef": deposit_ref,
        "DepositDate": deposit_date_iso,
        "BankAmount": bank_amt
    }

    # Power BI expects a list of rows
    data = json.dumps([row])

    try:
        response = requests.post(powerbi_url, data=data)
        if response.status_code != 200:
            print("Error pushing to Power BI:", response.text)
    except Exception as e:
        print("Exception while pushing to Power BI:", str(e))