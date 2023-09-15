#!/usr/bin/env python
"""
This is an MQTT client publishing helper module. Contains support and wrapper
functions for MQTT publishing.

Dependencies:
future
paho.mqtt.client
json
"""

# Module Info
__version__ = "1.0.1"
__all__ = [
    "generate_filename",
    "is_json_object",
    "is_json_string",
    "load_queue_from_file",
    "append_payload_to_queue",
    "save_json_mqtt_queue",
    "package_thingsboard_payload",
    "publish_mqtt_queue",
    "publish_to_thingsboard"
]


# Standard Imports
import os
import json

## Python 2/3 compatilibity standard imports
# int subclass of long on Py2, therefore int = long and short
# Allow encoding parameter in open()
from builtins import int, open

# Third party imports
import paho.mqtt.client
# import __main__ as main
import __main__

## Python 2/3 compatibility imports
# To print multiple strings, import print_function to prevent Py2 from interpreting it as a tuple:
# from __future__ import print_function


# Globals
# As per NETTY_MAX_PAYLOAD_SIZE from MQTT Broker/Thingsboard
MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE = 65536


# Error Code
MQTTHELPER_ERR_INVALID = 0
MQTTHELPER_ERR_EDGE = -2

# JSON Type
MQTTHELPER_JSON_DICT = 1
MQTTHELPER_JSON_ARRAY = 2


def generate_filename(filename=None):
    """
    Generate the filename for queue storage, file extension is not required.

    Args:
        filename (str, optional): Filename including file extension. Defaults to None.

    Returns:
        str: Filename including json extension. i.e filename.json
    """
    if filename is not None:
        filename = filename.strip()
    if filename is None or filename == "":
        # parent_filename = os.path.basename(main.__file__).rsplit('.', 1)[0]
        parent_filename = os.path.basename(__main__.__file__).rsplit('.', 1)[0]
        filename = "mqtt_queue_%s.json" % parent_filename
    return filename


def is_json_object(_object):
    """
    Check if object is of type dictionary or list of dictionary.

    Args:
        _object (any): Python object

    Returns:
        Literal[1, 2, 0]: Invalid - Zero Value. Dict - MQTTHELPER_JSON_DICT. \
            List of dictionary - MQTTHELPER_JSON_ARRAY
    """
    if isinstance(_object, dict):
        return MQTTHELPER_JSON_DICT
    if (isinstance(_object, list) and all(isinstance(item, dict) for item in _object)):
        return MQTTHELPER_JSON_ARRAY
    return MQTTHELPER_ERR_INVALID


# def is_json(text: str) -> bool:
def is_json_string(text):
    """
    Checks if string contains json document.
    Does not check if json document has valid structure.

    Args:
        text (str): String to test for json document

    Returns:
        Literal[1, 2, 0]: Invalid - Zero Value. Dict - MQTTHELPER_JSON_DICT. \
            List of dictionary - MQTTHELPER_JSON_ARRAY
    """
    if not text or not isinstance(text, (str, bytes, bytearray)):
        return MQTTHELPER_ERR_INVALID
    text = text.strip()
    if text and (text[0] in {'{', '['} and text[-1] in {'}', ']'}):
        try:
            return (is_json_object(json.loads(text)))
        except (ValueError, TypeError):
            # json.decoder.JSONDecodeError inherits from ValueError
            return MQTTHELPER_ERR_INVALID
    return MQTTHELPER_ERR_INVALID


def load_queue_from_file(filename):
    """
    Load json queue from file.

    Args:
        filename (str): Filename containing json queue

    Returns:
        list: JSON array
    """
    # Read backup JSON Data from previous failed uploads
    if os.path.isfile(filename):
        with open(filename, "r", encoding='utf-8') as json_file:
            try:
                json_queue = json.load(json_file)
                if isinstance(json_queue, dict):
                    return [json_queue]
                return json_queue
                # json_data_payload_size = len(json.dumps(json_data).encode("utf-8"))
            except ValueError:
                pass # JSON file is empty
    return []


def append_payload_to_queue(payload, json_queue):
    """
    Append json object to queue, modifies json_queue.

    Args:
        payload (dict | list | str): JSON object to append to queue
        queue (list): List containing json data

    Raises:
        ValueError: If payload format is not dict, list[dict] \
                    or json string format
    """
    json_type = is_json_object(payload)
    if MQTTHELPER_JSON_DICT == json_type:
        json_queue.append(payload)
    elif MQTTHELPER_JSON_ARRAY == json_type:
        # Expect a list of dictionary items
        json_queue.extend(payload)
    else:
        json_type = is_json_string(payload)
        if MQTTHELPER_JSON_DICT == json_type:
            json_queue.append(json.loads(payload))
        elif MQTTHELPER_JSON_ARRAY == json_type:
            # Expect a list of dictionary items
            json_queue.extend(json.loads(payload))
        else:
            raise ValueError("json payload format is invalid.")


# def save_json_mqtt_queue(filename, json_data, payload_index=None):
def save_json_mqtt_queue(filename, json_data, start=None, end=None):
    """
    Saves json mqtt queue to file.

    Args:
        filename: Name of JSON queue file archive, must include extension in filename, Default - None
        json_data: list of json data
        start_index: (Optional) List index to start saving from. Default: None
        end_index: (Optional) List index end to save to. Default: None
    """
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(json_data[start:end], json_file, indent=4, separators=(",", ": "))


def package_thingsboard_payload(data, ts=None):
    """
    Prepare payload for thingsboard.

    Args:
        data: JSON data for repackaging
        ts (int, optional): Timestamp in milliseconds since epoch. \
                            Defaults to None - ommits timestamp.

    Raises:
        TypeError: Timestamp not of numeric type.
        ValueError: Invalid payload format.

    Returns:
        dict: JSON payload with or without timestamp for thingsboard.
    """
    if ts is None:
        json_payload = data
    elif not isinstance(ts, (int, float)):
        raise TypeError("Expect ts to be of numeric type, received %s" % type(ts))
    else:
        if isinstance(data, dict):
            json_payload = {"ts":ts, "values": data}
        elif is_json_string(data):
            json_payload = {"ts":ts, "values": json.loads(data)}
        else:
            raise ValueError("json payload format is invalid.")

    return json_payload


# def publish_mqtt_queue(client: paho.mqtt.client, topic: str, json_payload: json doc,
#                       timeout: float, filename: str | None = None, debug=False) -> paho.mqtt.client.MQTTMessageInfo:
def publish_mqtt_queue(client, topic, json_payload, timeout=1.0, fifo=True,
                       filename=None, debug=False):
    """
    paho.mqtt.client.publish() helper to publish json payload with a qos=1 from
    a FIFO queue.
    Archived queue is stored in a json document file.

    Args:
        client: Connected paho.mqtt.client.Client()
        topic: Topic to publish to
        json_payload: JSON payload for appending to queue
        timeout: (Optional) Timeout to wait for publish ack in seconds, (Default - min of 1 second)
        fifo: (Optional) Declare behavior of queue, True (FIFO), FALSE (FILO) (Default - True)
        filename: (Optional) Name of JSON queue file archive, must include extension in filename, Default - None
        debug: (Optional) Flag to print each payload being published, Default - False

    Returns:
        paho.mqtt.client.MQTTMessageInfo of paho.mqtt.client.publish call

    Raises:
        ValueError: Invalid payload format.
    """
    timeout = max(timeout, 1.0)

    json_filename = generate_filename(filename=filename)

    # Read backup JSON Data from previous failed uploads
    json_data = load_queue_from_file(filename=json_filename)
    append_payload_to_queue(payload=json_payload, json_queue=json_data)

    # Loop through json data for publishing
    json_start = 0
    json_end = json_data_remain = subset_count = json_data_total_len = len(json_data)

    # print ("{0} {1} {2}".format(json_start, json_end, len(json.dumps(json_data[json_start:json_end]).encode("utf-8"))))
    while json_data_remain > 0:
        publish_success = False
        try:
            while len(json.dumps(json_data[json_start:json_end]).encode("utf-8")) > MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE:
                # Split payload in half until it fits
                subset_count = subset_count >> 1

                if debug:
                    print("Subset_Count: {0}".format(subset_count))

                # Unable to find a payload size that fits
                if subset_count == 0:
                    json_start = 0
                    json_end = json_data_total_len
                    raise RuntimeError(paho.mqtt.client.error_string(paho.mqtt.client.MQTT_ERR_PAYLOAD_SIZE))

                # Set correct index for subset group
                if fifo:
                    json_end = json_start + subset_count
                else:
                    json_start = json_end - subset_count

            # Result is in tuple (rc, mid) of MQTTMessageInfo class
            publish_result = client.publish(topic=topic, payload=json.dumps(json_data[json_start:json_end]), qos=1)
            # publish_result = paho.mqtt.client.MQTTMessageInfo
            publish_result.wait_for_publish(timeout=timeout)

            if debug:
                print("PayloadIndex: [{0}, {1}]".format(json_start, json_end))
                print("{0} {1}".format(publish_result, json_data[json_start:json_end]))
            # if publish_result.rc != paho.mqtt.client.MQTT_ERR_SUCCESS or not publish_result._published:
            #     break # Escape publishing loop on publish failure
            if not publish_result.is_published():
                break # Escape publishing loop on publish failure

        except (ValueError, RuntimeError) as error:
            print("PayloadIndex: [{0}, {1}] {2} {3}".format(json_start, json_end, type(error), error))
            break # Escape loop on error
        except Exception as error:
            print("MQTT Publish Error! PayloadIndex: [{0}, {1}] {2} {3}".format(json_start, json_end, type(error), error))
            # break # Escape loop on error
            raise  # Reraise error, unfortunately does not save to file queue
        else:
            publish_success = True
            ## Start iterate to next batch
            json_data_remain -= subset_count
            if debug:
                print("{0} {1} {2} {3}".format(json_start, json_end, json_data_remain, len(json.dumps(json_data[json_start:json_end]).encode("utf-8"))))
            if fifo:
                json_start = json_end
                json_end = min(json_end + subset_count, json_data_total_len)
            else:
                json_end = json_start
                json_start = max(json_start - subset_count, 0)

    # Test for edge case where published failed and info.rc returns success
    try:
        if not publish_success and publish_result.rc == paho.mqtt.client.MQTT_ERR_SUCCESS:
            # publish_result.rc = paho.mqtt.client.MQTT_ERR_UNKNOWN
            publish_result.rc = MQTTHELPER_ERR_EDGE
    except NameError:
        # publish_success = False
        publish_result = paho.mqtt.client.MQTTMessageInfo(0)
        publish_result.rc = paho.mqtt.client.MQTT_ERR_AGAIN

    # Process remaining items into file queue
    if publish_success and json_data_remain <= 0:
        # Clear the queue as all payloads was successfully published
        with open(filename, 'w', encoding='utf-8'):
            pass  # Do nothing, empty the file
    elif not publish_success:
        # Archive unsent data to file queue for sending later
        if fifo:
            print("Save fifo queue indexed [{0}:{1}]".format(json_start, None))
            save_json_mqtt_queue(filename=json_filename, json_data=json_data, start=json_start, end=None)
        else:
            print("Save filo queue indexed [{0}:{1}]".format(None, json_end))
            save_json_mqtt_queue(filename=json_filename, json_data=json_data, start=None, end=json_end)

    return publish_result

# publish_to_thingsboard: (client: paho.mqtt.client.Client(), payload: str,
#                           ts: int | None = None, timeout: float = 1,
#                           filename: str | None = None, display_payload: bool = False,
#                           debug: bool = False) -> paho.mqtt.client.MQTTMessageInfo:
def publish_to_thingsboard(client, payload, ts=None, fifo=False,
                           timeout=1.0, filename=None, display_payload=False, debug=False):
    """
    paho.mqtt.client.publish() helper to publish to thingsboard using
    publish_mqtt_queue() helper function.
    Implements payload archiving queue.

    Args:
        client: Connected paho.mqtt.client.Client()
        payload: JSON payload for appending to queue
        ts: (Optional) Timestamp in milliseconds from epoch, Default - None, ommits timestamp
        timeout: (Optional) Timeout to wait for publish ack in seconds, (Default - min of 1 second)
        fifo: (Optional) Declare behavior of queue, True (FIFO), FALSE (FILO) (Default - False)
        filename: (Optional) Name of JSON queue file archive, must include extension in filename, Default - None
        display_payload: (Optional) Displays the current payload to be appended, Default - False
        debug: (Optional) Flag to print each payload being published, Default - False

    Returns:
        paho.mqtt.client.MQTTMessageInfo of paho.mqtt.client.publish call

    Raises:
        ValueError: Invalid payload format.
        TypeError: Timestamp not of numeric type.
    """
    current_json_data = package_thingsboard_payload(data=payload, ts=ts)

    if display_payload:
        print(json.dumps(current_json_data))

    publish_result = publish_mqtt_queue(client=client, topic="v1/devices/me/telemetry",
                                        json_payload=current_json_data, timeout=timeout, fifo=fifo,
                                        filename=filename, debug=debug)
    return publish_result
