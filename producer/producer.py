import os
import json
import time  # This is a built-in module, no need to install
from datetime import datetime
import pytz  # For better timezone handling
import requests
from dotenv import load_dotenv
from kafka import KafkaProducer
import schedule

load_dotenv()

def get_current_timestamp():
    return datetime.now(pytz.utc).strftime("%Y-%m-%d_%H-%M-%S")

def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relative_humidity_2m,rain,wind_speed_10m,soil_temperature_6cm"
    response = requests.get(url)
    return response.json()
# def fetch_weather_data():
#     url = "https://api.data.gov.sg/v1/environment/air-temperature"
#     response = requests.get(url)
#     return response.json()

def save_to_json(data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs('json', exist_ok=True)
    filename = f"json/data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved weather data to {filename}")

def send_to_kafka(data):
    producer = KafkaProducer(
        bootstrap_servers=[os.getenv('KAFKA_BROKER')],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    producer.send(os.getenv('TOPIC_NAME'), value=data)
    producer.flush()
    print("Sent data to Kafka")

def job():
    print("Fetching weather data...")
    try:
        weather_data = fetch_weather_data()
        save_to_json(weather_data)
        send_to_kafka(weather_data)
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Run immediately on start
    job()

    # Schedule to run every hour
    schedule.every(1).hour.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()