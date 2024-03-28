import requests
import time
from random import uniform
import argparse

def generate_sensor_data(sensor_id, sensor_type, min_value, max_value, unit):
    """
    Generates a reading data message based on the specified range.
    """
    reading = uniform(min_value, max_value)
    
    # Construct the message
    message = {
        "sensor_id": sensor_id,
        "sensor_type": sensor_type,
        "data": {
            "value": round(reading, 2),
            "unit": unit
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    return message

def send_sensor_data(sensor_id, sensor_type, min_value, max_value, unit, url, headers):
    """
    Sends sensor data to the specified URL every second.
    """
    while True:
        data = generate_sensor_data(sensor_id, sensor_type, min_value, max_value, unit)
        
        payload = {"records": [{"value": data}]}
        
        response = requests.post(url, json=payload, headers=headers)
        print(20*"_")
        print(f"Data sent: {data}")
        print(f"Response: {response.status_code}, {response.text}")
        
        time.sleep(1)

def main():
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

    send_sensor_data(args.sensor_id, args.sensor_type, args.min_value, args.max_value, args.unit, url, headers)

if __name__ == "__main__":
    main()
