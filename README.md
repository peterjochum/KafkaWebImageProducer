# Kafka Web Image Producer

Downloads images from a HTTP source and sends them to a kafka topic.

## Usage

### Environment

- BOOTSTRAP_SERVERS list of Kafka bootstrap servers to connect to
- RETRIEVE_INTERVAL image retrieval interval (default:60)

### Configure the camera

```json
{
  "camID": "2",
  "desc": "test_description",
  "url": "http://testurl.com",
  "area": [[1, 2], [3, 4]]
}
```

- **camID** Unique ID of the camera - used for partitioning
- **desc** Description/location/additional information of the camera
- **url** Camera image URL
- **area** Area of interest. For example a single lane of a highway camera. Polygon of pixel coordinates.


### Run the container

To run the container locally use `--network-host`

```shell
docker run --network=host -e BOOTSTRAP_SERVERS="localhost:9092" --rm kafkawebimageproducer:local
```
