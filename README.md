# SiteVisor Sensors
This repository contains code for sensors used in the [SiteVisor Project](https://github.com/grzpiotrowski/sitevisor-project).

## Sensors list
### [Simulated environmental sensor](./simulated-env-sensor.py)

This code randomly generates simple data within the specified range and sends it to a Kafka Broker accesible over HTTP via Kafka Bridge.

Setup dependencies:
```bash
pip install -r requirements.txt
```

Example usage:
```bash
python .\simulated_env_sensor.py --topic='my-topic' --sensor-id='sensor-42' --min-value=10.0 --max-value=30.0 --sensor-type='temperature' --unit='C'
```

To run mutliple simulated sensors at once:
```bash
python run_multiple_sim_sensors.py --num-sensors=5 --topic='my-topic' --base-min-value=15.0 --base-max-value=25.0 --sensor-type='temperature' --unit='C'
```

### DHT11 Sensor with Raspberry Pi 4B
Script to read data from DHT11 sensor on GPIO04 and send it to Kafka Bridge.

#### Setup
Recommended to setup a new [venv](https://docs.python.org/3/library/venv.html). Then install dependencies:
```bash
pip install -r requirements_rpi.txt
```

Example usage:
```bash
python sitevisor_dht11_sensor.py --topic='my-topic' --sensor-id='dht11' --ip='sitevisor.local'
```



## References
[Using the DHT11 Sensor on the Raspberry Pi](https://pimylifeup.com/raspberry-pi-dht11-sensor/)