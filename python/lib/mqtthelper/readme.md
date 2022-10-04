# mqtthelper: paho.mqtt.client Helper module
This is an MQTT client publishing python helper module.
Contains support and wrapper functions for MQTT publishing.

# Dependencies
* paho.mqtt.client
* json

# Usage and API
```python
import mqtthelper
```

## is_json_string()
```python
is_json_string(text)
```
Checks if the string object contains json document. Does not check if json document has valid structure
### Params
* `text` - String to test for json document


## publish_mqtt_queue()
```python
publish_mqtt_queue(client, topic, json_payload, timeout=1.0, filename=None, debug=False):
```
paho.mqtt.client.publish() wrapper to publish json payload with a qos=1 from a FIFO queue. Archived queue is stored in a json document file.

### Params
* `client` - The connected paho.mqtt.client.Client() to publish on.
* `topic` - MQTT topic to publish to.
* `json_payload` - JSON payload to append to a queue for sending
* `timeout` - (Optional) Blocking time per publish instruction in seconds, minimum of 1.0 set
* `filename` - (Optional) JSON file to store payload queue on unsuccessfull publish. Defaults to the calling `mqtt_queue_<callingscript>.json` if filename is not given or empty.
* `debug` - (Optional) Flag to print to screen the `MQTTMessageInfo()` and payload from each paho.mqtt.client.publish() call. Defaults: False

### Returns
paho.mqtt.client.MQTTMessageInfo from the last publishing call.

### Raises
`ValueError` if payload format is not appropriate.


## publish_to_thingsboard()
```python
publish_to_thingsboard(client, payload, ts=None, timeout=1.0, filename=None, display_payload=False, debug=False)
```
paho.mqtt.client.publish() helper for publish to thingsboard using publish_mqtt_queue() helper function. Implements payload archiving queue.

### Params
* `client` - The connected paho.mqtt.client.Client() to publish on.
* `payload` - JSON payload to append to a queue for sending
* `ts` - Timestamp in milliseconds from epoch, if ts=None, payload is sent without timestamp.
* `timeout` - (Optional) Blocking time per publish instruction in seconds, minimum of 1.0 set
* `filename` - (Optional) JSON file to store payload queue on unsuccessfull publish. Defaults to the calling `mqtt_queue_<callingscript>.json` if filename is not given or empty.
* `display_payload` - (Optional) Displays the current payload to be appended. Defaults: False
* `debug` - (Optional) Flag to print to screen the `MQTTMessageInfo()` and payload from each paho.mqtt.client.publish() call. Defaults: False

### Returns
paho.mqtt.client.MQTTMessageInfo from the last publishing call.

### Raises
`ValueError` if payload format is not appropriate or `TypeError` if timestamp is not numeric.