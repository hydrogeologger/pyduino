<!-- markdownlint-disable -->

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

# <kbd>module</kbd> `mqtthelper`
This is an MQTT client publishing helper module providing file base queue redundancy support.

Contains support and wrapper functions for MQTT publishing and publishing to
thingsboard.

Dependencies:
- paho-mqtt : paho.mqtt.client


## Table of Contents
- [`append_payload_to_queue`](./mqtthelper.md#function-append_payload_to_queue): Append json object to queue, modifies json_queue.
- [`generate_filename`](./mqtthelper.md#function-generate_filename): Generate the filename for queue storage.
- [`is_json_object`](./mqtthelper.md#function-is_json_object): Check if object is of type dictionary or list of dictionary.
- [`is_json_string`](./mqtthelper.md#function-is_json_string): Checks if string contains json document.
- [`load_queue_from_file`](./mqtthelper.md#function-load_queue_from_file): Load json queue from file.
- [`package_thingsboard_payload`](./mqtthelper.md#function-package_thingsboard_payload): Prepare payload for thingsboard.
- [`publish_mqtt_queue`](./mqtthelper.md#function-publish_mqtt_queue): paho.mqtt.client.publish() helper to publish json payload from queue.
- [`publish_to_thingsboard`](./mqtthelper.md#function-publish_to_thingsboard): paho.mqtt.client.publish() helper publishing to thingsboard with payload queueing.
- [`save_queue_to_file`](./mqtthelper.md#function-save_queue_to_file): Saves json mqtt queue to file.


**Global Variables**
---------------
- **MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE** = 65536
- **MQTTHELPER_ERR_INVALID** = 0
- **MQTTHELPER_ERR_EDGE** = -2
- **MQTTHELPER_JSON_DICT** = 1
- **MQTTHELPER_JSON_ARRAY** = 2

---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `generate_filename`

```python
generate_filename(filename=None)
```

Generate the filename for queue storage.


**Args:**

- <b>`filename`</b> (str, optional): Filename including file extension. Defaults to None.


**Returns:**

- <b>`str`</b>: Filename including extension. i.e mqtt_queue_callingscriptname.json.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L112"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `is_json_object`

```python
is_json_object(object_)
```

Check if object is of type dictionary or list of dictionary.


**Args:**

- <b>`object_`</b> (any): Python object.


**Returns:**

- <b>`Literal[0, 1, 2]`</b>: Literal value representing valid json object.

    - Invalid - 0, MQTTHELPER_ERR_INVALID.
    - Dict - 1, MQTTHELPER_JSON_DICT.
    - List of dictionary - 2, MQTTHELPER_JSON_ARRAY.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L133"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `is_json_string`

```python
is_json_string(text)
```

Checks if string contains json document.

Does not check if json document has valid structure.


**Args:**

- <b>`text`</b> (str): String to test for json document.


**Returns:**

- <b>`Literal[0, 1, 2]`</b>: Literal value representing valid json string.

    - Invalid - 0, MQTTHELPER_ERR_INVALID.
    - Dict - 1, MQTTHELPER_JSON_DICT.
    - List of dictionary - 2, MQTTHELPER_JSON_ARRAY.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `load_queue_from_file`

```python
load_queue_from_file(filepath)
```

Load json queue from file.


**Args:**

- <b>`filepath`</b> (str): File path containing json queue.


**Returns:**

- <b>`list`</b>: JSON array.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L185"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `append_payload_to_queue`

```python
append_payload_to_queue(payload, json_queue)
```

Append json object to queue, modifies json_queue.


**Args:**

- <b>`payload`</b> (dict | list | str): JSON object to append to queue.
- <b>`queue`</b> (list): List containing json data.


**Raises:**

- <b>`ValueError`</b>: If payload format is not dict, list[dict] or json string format.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L214"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `save_queue_to_file`

```python
save_queue_to_file(filepath, json_queue, start=None, end=None)
```

Saves json mqtt queue to file.


**Args:**

- <b>`filename`</b> (str): Name of JSON queue file archive, must include
    extension in filename.
- <b>`json_queue`</b> (list): List of json data.
- <b>`start`</b> (int, optional): List index to start saving from.. Defaults to None.
- <b>`end`</b> (int, optional): List index end to save to. Defaults to None.


**Raises:**

- <b>`TypeError: json_queue not an array of json (key`</b>: value) data.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L241"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `publish_mqtt_queue`

```python
publish_mqtt_queue(
    client,
    topic,
    json_queue,
    timeout=1.0,
    fifo=False,
    debug=False,
    max_payload_bytes=65536
)
```

paho.mqtt.client.publish() helper to publish json payload from queue.

Publishing is performed with qos=1.
Calling publish_mqtt_queue will modify json_queue.


**Args:**

- <b>`client`</b> (Client): MQTT Client.
- <b>`topic`</b> (str): MQTT Topic to publish to.
- <b>`json_queue`</b> (list[dict]): JSON array queue for publishing, will be modified.
- <b>`timeout`</b> (float|int, optional): Timeout to wait for publish ack in
    seconds. Defaults to 1.0.
- <b>`fifo`</b> (bool, optional): Declare behavior of queue,
    True (FIFO), FALSE (FILO). Defaults to False.
- <b>`debug`</b> (bool, optional): Flag to print each payload being published.
    Defaults to False.
- <b>`max_payload_bytes`</b> (int, optional): Max size of payload per transmit cycle.
    Defaults to MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE.


**Raises:**

- <b>`RuntimeError`</b>: General exception.


**Returns:**

- <b>`paho.mqtt.client.MQTTMessageInfo`</b>: Publish result.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L355"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `package_thingsboard_payload`

```python
package_thingsboard_payload(data, ts=None)
```

Prepare payload for thingsboard.


**Args:**

- <b>`data`</b>: JSON data for repackaging.
- <b>`ts`</b> (int, optional): UTC Timestamp in milliseconds since epoch.
    Defaults to None - ommits timestamp.


**Raises:**

- <b>`TypeError`</b>: Timestamp not of numeric type.
- <b>`ValueError`</b>: Invalid payload format.


**Returns:**

- <b>`dict|None`</b>: JSON payload with or without timestamp for thingsboard.
    Returns None if no data was attempted to be packaged.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L391"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `publish_to_thingsboard`

```python
publish_to_thingsboard(
    client,
    payload,
    ts=None,
    fifo=False,
    timeout=3.0,
    filename=None,
    display_payload=False,
    debug=False,
    max_payload_bytes=65536
)
```

paho.mqtt.client.publish() helper publishing to thingsboard with payload queueing.

Implements payload file archiving queue.


**Args:**

- <b>`client`</b> (paho.mqtt.client.Client()): MQTT client
- <b>`payload`</b> (dict): JSON payload for appending to queue
- <b>`ts`</b> (int, optional): Timestamp in milliseconds from epoch.
    Default - None, ommits timestamp
- <b>`fifo`</b> (bool, optional): Declare behavior of queue,
    True (FIFO), False (FILO). Defaults to False.
- <b>`timeout`</b> (float, optional): Timeout to wait for publish ack in seconds.
    Defaults to 3.0.
- <b>`filename`</b> (str, optional): _description_. Defaults to None.
- <b>`display_payload`</b> (bool, optional): Name of JSON queue file archive,
    must include extension in filename. Defaults to False.
- <b>`debug`</b> (bool, optional): Flag to print each payload being published.
    Defaults to False.
- <b>`max_payload_bytes`</b> (int, optional): Max size of payload per transmit cycle.
    Defaults to MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE.


**Raises:**

- <b>`ValueError`</b>: Invalid payload format.
- <b>`TypeError`</b>: Timestamp not of numeric type.


**Returns:**

- <b>`paho.mqtt.client.MQTTMessageInfo`</b>: Publish result.



