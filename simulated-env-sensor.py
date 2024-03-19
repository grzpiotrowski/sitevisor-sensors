import requests
import time
from random import uniform
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Send simulated sensor data to Kafka.')
parser.add_argument('--topic', type=str, default='my-topic', help='Kafka topic name')
parser.add_argument('--sensor-id', type=str, default='sensor-12345', help='Sensor ID')
parser.add_argument('--sensor-type', type=str, default='temperature', help='Type of sensor')
parser.add_argument('--unit', type=str, default='C', help='Reading Unit')
parser.add_argument('--min-value', type=float, default=20.0, help='Minimum reading for data generation')
parser.add_argument('--max-value', type=float, default=30.0, help='Maximum reading for data generation')

args = parser.parse_args()

# URL of the Kafka Bridge
url = f'http://localhost:8080/topics/{args.topic}'

# Headers for the POST request
headers = {
    'Content-Type': 'application/vnd.kafka.json.v2+json'
}

def generate_sensor_data():
    """
    Generates a reading data message based on the specified range.
    """
    reading = uniform(args.min_value, args.max_value)
    
    # Construct the message
    message = {
        "sensor_id": args.sensor_id,
        "sensor_type": args.sensor_type,
        "data": {
            "value": round(reading, 2),
            "unit": args.unit
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    return message

def send_sensor_data():
    """
    Sends sensor data to the specified URL every second.
    """
    while True:
        data = generate_sensor_data()
        
        payload = {"records": [{"value": data}]}
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Data sent: {data}")
        print(f"Response: {response.status_code}, {response.text}")
        
        time.sleep(1)

if __name__ == "__main__":
    send_sensor_data()
