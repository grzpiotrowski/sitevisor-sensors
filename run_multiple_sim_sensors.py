import threading
import argparse
from random import uniform
from simulated_env_sensor import send_sensor_data

# Parse command line arguments for the runner script
parser = argparse.ArgumentParser(description='Run multiple simulated sensors.')
parser.add_argument('--num-sensors', type=int, default=5, help='Number of sensors to simulate')
parser.add_argument('--topic', type=str, default='my-topic', help='Kafka topic name')
parser.add_argument('--sensor-type', type=str, default='temperature', help='Type of sensor')
parser.add_argument('--unit', type=str, default='C', help='Reading Unit')
parser.add_argument('--base-min-value', type=float, default=10.0, help='Base minimum reading for data generation')
parser.add_argument('--base-max-value', type=float, default=30.0, help='Base maximum reading for data generation')
parser.add_argument('--url', type=str, default='http://localhost:8080/topics/', help='URL of the Kafka Bridge')

args = parser.parse_args()

# Headers for the POST request
headers = {
    'Content-Type': 'application/vnd.kafka.json.v2+json'
}

# URL of the Kafka Bridge
topic_url = f'{args.url}{args.topic}'

# Function to run a sensor
def run_sensor(sensor_id, min_value, max_value):
    send_sensor_data(sensor_id, args.sensor_type, min_value, max_value, args.unit, topic_url, headers)

# Start each sensor in a separate thread
# Each with slightly varying data range
for i in range(args.num_sensors):
    sensor_id = f'sensor-{i+1}'
    range_variance = uniform(0, i+1)
    min_value = args.base_min_value + range_variance
    max_value = args.base_max_value + range_variance
    t = threading.Thread(target=run_sensor, args=(sensor_id, min_value, max_value))
    t.start()
