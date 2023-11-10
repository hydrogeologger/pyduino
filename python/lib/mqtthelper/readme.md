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

## generate_filename()
```python
generate_filename(filename=None)
```
Returns the filename for queue storage, file extension is not required.
### Params
* `filename` - Filename including file extension. Defaults to None.


## is_json_object()
```python
is_json_object(object_)
```
Check if object is of type dictionary or list of dictionary.
### Params
* `object_` - Object to test for json style
### Returns
Return literals, `MQTTHELPER_ERR_INVALID` - 0, `MQTTHELPER_JSON_DICT` - 1, `MQTTHELPER_JSON_ARRAY` - 2


## is_json_string()
```python
is_json_string(text)
```
Checks if the string object contains json document.
### Params
* `text` - String to test for json document
### Returns
Return literals, `MQTTHELPER_ERR_INVALID` - 0, `MQTTHELPER_JSON_DICT` - 1, `MQTTHELPER_JSON_ARRAY` - 2


## load_queue_from_file()
```python
load_queue_from_file(filename)
```
Load the json queue from file
### Params
* `filename` - Filename with file extension, containing json queue.
### Returns
JSON queue list


## append_payload_to_queue()
```python
append_payload_to_queue(payload, json_queue)
```
Append json object to queue, json_queue is modified.
### Params
* `payload` - JSON object to append to queue
* `queue` - List containing json data
### Raises
`ValueError` if payload format is invalid.

## save_queue_to_file()
```python
save_queue_to_file(filename, json_queue, start=None, end=None)
```
Saves json mqtt queue to file.
### Params
* `filename` - JSON object to append to queue
* `json_queue` - List containing json data.
* `start` - (Optional) List index to start saving from.. Defaults to None.
* `end` - (Optional) List index end to save to. Defaults to None.


## publish_mqtt_queue()
```python
publish_mqtt_queue(client, topic, json_queue, timeout=1.0, fifo=True, debug=False)
```
paho.mqtt.client.publish() helper to publish json payload with a qos=1 from
    a queue.
    Calling publish_mqtt_queue will modify json_queue.

### Params
* `client` - The connected paho.mqtt.client.Client() to publish on.
* `topic` - MQTT topic to publish to.
* `json_queue` - JSON queue to publish.
* `timeout` - (Optional) Blocking time per publish instruction in seconds, minimum of 1.0 set
* `fifo` - (Optional) Behavior of queue to be used, True (FIFO), False (FILO). Defaults to True.
* `debug` - (Optional) Flag to print to screen the `MQTTMessageInfo()` and payload from each paho.mqtt.client.publish() call. Defaults: False

### Returns
paho.mqtt.client.MQTTMessageInfo from the last publishing call.

### Raises
`RuntimeError` JSON queue or subset of queue is larger than `MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE`.


## publish_to_thingsboard()
```python
publish_to_thingsboard(client, payload, ts=None,
                       fifo=False, timeout=3.0, filename=None, 
                       display_payload=False, debug=False)
```
paho.mqtt.client.publish() helper for publish to thingsboard using publish_mqtt_queue() helper function. Implements payload archiving queue.
No need to call `package_thingsboard_payload()` if using this function.

### Params
* `client` - The connected paho.mqtt.client.Client() to publish on.
* `payload` - JSON payload to append to a queue for sending
* `ts` - Timestamp in milliseconds from epoch, if ts=None, payload is sent without timestamp.
* `fifo` - (Optional) Behavior of queue to be used, True (FIFO), False (FILO). Defaults to False.
* `timeout` - (Optional) Blocking time per publish instruction in seconds, minimum of 1.0 set. Default - 3 seconds.
* `filename` - (Optional) JSON file to store payload queue on unsuccessfull publish. Defaults to the calling `mqtt_queue_<callingscript>.json` if filename is not given or empty.
* `display_payload` - (Optional) Displays the current payload to be appended. Defaults: False
* `debug` - (Optional) Flag to print to screen the `MQTTMessageInfo()` and payload from each paho.mqtt.client.publish() call. Defaults: False

### Returns
paho.mqtt.client.MQTTMessageInfo from the last publishing call.

### Raises
`ValueError` if payload format is not appropriate or `TypeError` if timestamp is not numeric.


## package_thingsboard_payload()
```python
package_thingsboard_payload(data, ts=None)
```
Prepare payload for thingsboard to include or omit timestamp.
Do not use `package_thingsboard_payload` to package the payload for `publish_to_thingsboard`

### Params
* `data` - JSON data for repackaging
* `ts` - (Optional) Timestamp in milliseconds from epoch, Default - None, ommits 

### Returns
JSON payload for thingsboard

### Raises
`ValueError` if payload format is not appropriate or `TypeError` if timestamp is not numeric.
