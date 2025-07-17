import os
import json
from kafka import KafkaConsumer
from datetime import datetime

# Make sure the same topic name is used
TOPIC_NAME = os.getenv('TOPIC_NAME', 'weather_topic')
BOOTSTRAP_SERVERS = os.getenv('KAFKA_BROKER', 'localhost:9092')

# Setup Kafka Consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[BOOTSTRAP_SERVERS],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='weather_json_saver'
)

# Make directory if not exists
os.makedirs("kafka_output", exist_ok=True)

print("Listening to Kafka and saving incoming messages...")

for message in consumer:
    data = message.value
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'kafka_output/data_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved message to {filename}")
