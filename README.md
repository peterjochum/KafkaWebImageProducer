# Kafka Web Image Producer

Downloads images from a HTTP source and sends them to a kafka topic.

## Usage

### Environment

- BOOTSTRAP_SERVERS list of Kafka bootstrap servers to connect to
- RETRIEVE_INTERVAL image retrieval interval (default:60)

### Run the container

To run the container locally use `--network-host`

```shell
docker run --network=host -e BOOTSTRAP_SERVERS="localhost:9092" --rm kafkawebimageproducer:local
```
