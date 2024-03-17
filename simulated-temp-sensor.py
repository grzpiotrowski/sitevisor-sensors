import requests
import time
from random import uniform

# URL of the Kafka Bridge
url = 'http://sitevisor.local:8080/topics/my-topic'

# Headers for the POST request
headers = {
    'Content-Type': 'application/vnd.kafka.json.v2+json'
}

def generate_temperature_data():
    """
    Generates a temperature data message.
    """
    temperature = uniform(20.0, 30.0)
    
    # Construct the message
    message = {
        "sensor_id": "sensor-12345",
        "sensor_type": "temperature",
        "data": {
            "value": round(temperature, 2),
            "unit": "C"
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    return message

def send_temperature_data():
    """
    Sends temperature data to the specified URL every second.
    """
    while True:
        data = generate_temperature_data()
        
        payload = {"records": [{"value": data}]}
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Data sent: {data}")
        print(f"Response: {response.status_code}, {response.text}")
        
        time.sleep(1)

if __name__ == "__main__":
    send_temperature_data()
