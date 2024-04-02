import time
import adafruit_dht
import board
import requests
import argparse

def read_dht_data(dht_sensor):
    try:
        temperature_c = dht_sensor.temperature
        humidity = dht_sensor.humidity

        print("Temp:{:.1f} C, Humidity: {}%".format(temperature_c, humidity))

        return { "temperature": temperature_c, "humidity": humidity }
        
    except RuntimeError as error:
        print(error.args[0])
        return False


def main():
    dht_sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)

    parser = argparse.ArgumentParser(description='Send simulated sensor data to Kafka.')
    parser.add_argument('--topic', type=str, default='my-topic', help='Kafka topic name')
    parser.add_argument('--sensor-id', type=str, default='dht-11', help='Sensor ID')
    parser.add_argument('--ip', type=str, default='sitevisor.local', help='Sitevisor IP')

    args = parser.parse_args()

    url = f'http://{args.ip}:8080/topics/{args.topic}'

    headers = {
        'Content-Type': 'application/vnd.kafka.json.v2+json'
    }

    while True:
        dht_readings = read_dht_data(dht_sensor)

        if dht_readings != False:
            message_temp = {
                "sensor_id": args.sensor_id,
                "sensor_type": "temperature",
                "data": {
                    "value": dht_readings["temperature"],
                    "unit": "C"
                },
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

            payload_temp = {"records": [{"value": message_temp}]}
            
            response = requests.post(url, json=payload_temp, headers=headers)
            print(20*"_")
            print(f"Data sent: {message_temp}")
            print(f"Response: {response.status_code}, {response.text}")

            message_humidity = {
                "sensor_id": f"{args.sensor_id}-humidity",
                "sensor_type": "humidity",
                "data": {
                    "value": dht_readings["humidity"],
                    "unit": "%"
                },
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

            payload_humidity = {"records": [{"value": message_humidity}]}
            
            response = requests.post(url, json=payload_humidity, headers=headers)
            print(20*"_")
            print(f"Data sent: {message_humidity}")
            print(f"Response: {response.status_code}, {response.text}")

        time.sleep(1)



if __name__ == "__main__":
    main()