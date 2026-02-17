# kafka_producer.py
from kafka import KafkaProducer
import json, time, random
from datetime import datetime

# Configure Kafka connection
producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = "payments_real_time"

print("🚀 Producing payment messages to Kafka... (Ctrl+C to stop)\n")

while True:
    # Simulated payment event
    payment = {
        "DepositDate": datetime.now().strftime("%Y-%m-%d"),
        "PaymentCount": random.randint(1, 20),
        "TotalBankAmount": round(random.uniform(1000, 10000), 2)
    }

    producer.send(topic, payment)
    print("Produced:", payment)

    # Wait before sending the next record (adjust as needed)
    time.sleep(3)


