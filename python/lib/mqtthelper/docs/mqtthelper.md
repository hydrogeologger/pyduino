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
- [`generate_queue_filepath`](./mqtthelper.md#function-generate_queue_filepath): Generate the file path for queue storage.
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

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `generate_queue_filepath`

```python
generate_queue_filepath(filepath=None)
```

Generate the file path for queue storage.


**Args:**

- <b>`filepath`</b> (str, optional): File path including file extension. Defaults to None.


**Returns:**

- <b>`str`</b>: File path including extension. i.e absolute/path/to/mqtt_queue_callingscriptname.json.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `is_json_object`

```python
is_json_object(object_)
```

Check if object is of type dictionary or list of dictionary.


**Args:**

- <b>`object_`</b> (any): Python object.


**Returns:**

- <b>`int`</b>: Literal value representing valid json object.

    - Invalid - 0, MQTTHELPER_ERR_INVALID.
    - Dict - 1, MQTTHELPER_JSON_DICT.
    - List of dictionary - 2, MQTTHELPER_JSON_ARRAY.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L136"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `is_json_string`

```python
is_json_string(text)
```

Checks if string contains json document.

Does not check if json document has valid structure.


**Args:**

- <b>`text`</b> (str): String to test for json document.


**Returns:**

- <b>`int`</b>: Literal value representing valid json string.

    - Invalid - 0, MQTTHELPER_ERR_INVALID.
    - Dict - 1, MQTTHELPER_JSON_DICT.
    - List of dictionary - 2, MQTTHELPER_JSON_ARRAY.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `load_queue_from_file`

```python
load_queue_from_file(filepath)
```

Load json queue from file.


**Args:**

- <b>`filepath`</b> (str): File path containing json queue.


**Returns:**

- <b>`list[dict]`</b>: JSON array.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L188"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `append_payload_to_queue`

```python
append_payload_to_queue(payload, json_queue)
```

Append json object to queue, modifies json_queue.


**Args:**

- <b>`payload`</b> (dict | list[dict] | str): JSON object to append to queue.
- <b>`queue`</b> (list): List containing json data.


**Raises:**

- <b>`ValueError`</b>: If payload format is not dict, list[dict] or json string format.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L217"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

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
    True (FIFO), FALSE (LIFO). Defaults to False.
- <b>`debug`</b> (bool, optional): Flag to print each payload being published.
    Defaults to False.
- <b>`max_payload_bytes`</b> (int, optional): Max size of payload per transmit cycle.
    Defaults to MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE.


**Raises:**

- <b>`RuntimeError`</b>: General exception.


**Returns:**

- <b>`paho.mqtt.client.MQTTMessageInfo`</b>: Iterable object that contains information about the published message.
    Such that (rc, mid) = client.publish(...) is still valid.
    - mid (int): The message ID.
    - rc (int): The result code of the publish call.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L361"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `package_thingsboard_payload`

```python
package_thingsboard_payload(data, ts=None)
```

Prepare payload for thingsboard.


**Args:**

- <b>`data`</b>: JSON data for repackaging.
- <b>`ts`</b> (int, optional): UTC Timestamp in milliseconds since epoch.
    Defaults to None - omits timestamp.


**Raises:**

- <b>`TypeError`</b>: Timestamp not of numeric type.
- <b>`ValueError`</b>: Invalid payload format.


**Returns:**

- <b>`dict|None`</b>: Returns None if no data was attempted to be packaged.
    Dictionary as per thingsboard JSON object will include:
    If includes timestamp:
    - "ts" (int): Timestamp in milliseconds since epoch.
    - "values" (dict): Dictionary containing key: value pair data.
    If no timestamp: Standard dictionary containing key: value pair data.



---

<a href="../../../../python/lib/mqtthelper/src/mqtthelper/__init__.py#L401"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square" /></a>

## <kbd>function</kbd> `publish_to_thingsboard`

```python
publish_to_thingsboard(
    client,
    payload,
    ts=None,
    fifo=False,
    timeout=3.0,
    filename=None,
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
    Default - None, omits timestamp
- <b>`fifo`</b> (bool, optional): Declare behavior of queue,
    True (FIFO), False (LIFO). Defaults to False.
- <b>`timeout`</b> (float, optional): Timeout to wait for publish ack in seconds.
    Defaults to 3.0.
- <b>`filepath`</b> (str, optional): Name of JSON queue file archive file path,
    must include extension in filename/path. Defaults to None.
- <b>`debug`</b> (bool, optional): Flag to print each payload being published.
    Defaults to False.
- <b>`max_payload_bytes`</b> (int, optional): Max size of payload per transmit cycle.
    Defaults to MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE.


**Raises:**

- <b>`ValueError`</b>: Invalid payload format.
- <b>`TypeError`</b>: Timestamp not of numeric type.


**Returns:**

- <b>`tuple[MQTTMessageInfo,dict|None]`</b>: A tuple containing:
    - paho.mqtt.client.MQTTMessageInfo: Iterable object that contains information about the published message.
        - mid (int): The message ID.
        - rc (int): The result code of the publish call.
    - dict | None: Dictionary of constructed payload or None if payload is empty.



