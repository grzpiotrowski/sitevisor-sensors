# SiteVisor Sensors
This repository contains code for sensors used in the [SiteVisor Project](https://github.com/grzpiotrowski/sitevisor-project).

## Sensors list
### [Simulated environmental sensor](./simulated-env-sensor.py)

This code randomly generates simple data within the specified range and sends it to a Kafka Broker accesible over HTTP via Kafka Bridge.

Example usage:
```bash
python .\simulated_env_sensor.py --topic='my-topic' --sensor-id='sensor-42' --min-value=10.0 --max-value=30.0 --sensor-type='temperature' --unit='C'
```

To run mutliple sensors at once:
```bash
python run_multiple_sim_sensors.py --num-sensors=5 --topic='my-topic' --base-min-value=15.0 --base-max-value=25.0 --sensor-type='temperature' --unit='C'
```