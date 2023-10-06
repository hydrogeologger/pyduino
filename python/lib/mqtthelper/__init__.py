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
    "save_queue_to_file",
    "package_thingsboard_payload",
    "publish_mqtt_queue",
    "publish_to_thingsboard"
]


# Standard Imports
import os
import sys
import json

## Python 2/3 compatilibity standard imports
# from builtins import int, open

# Third party imports
import paho.mqtt.client
# import __main__ as main
import __main__


## Python 2/3 Compatibility Support
# The long builtin no longer exists in Python3.
if sys.version_info >= (3,0):
    long = int

# To print multiple strings, import print_function to prevent Py2 from interpreting it as a tuple:
# from __future__ import print_function
# Allow encoding parameter in open()
def do_open(file, mode, encoding, *args, **kwargs):
    """Wrapper for builtin python open() compatibility between python2 and python3.
    Removes encoding argument from open() for python2

    Args:
        file (FileDescriptorOrPath): File descriptor or path
        mode (str): File open mode

    Returns:
        fileobject: File objet
    """
    if sys.version_info.major >= 3:
        return open(file, mode, *args, encoding = encoding, **kwargs)
    if "encoding" in kwargs:
        del kwargs["encoding"]
    return open(file, mode, *args, **kwargs)  # pylint: disable=unspecified-encoding


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
        with do_open(filename, "r", encoding='utf-8') as json_file:
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
def save_queue_to_file(filename, json_queue, start=None, end=None):
    """
    Saves json mqtt queue to file.

    Args:
        filename (str): Name of JSON queue file archive, must include \
                        extension in filename.
        json_queue (list): List of json data.
        start (int, optional): List index to start saving from.. Defaults to None.
        end (int, optional): List index end to save to. Defaults to None.

    Raises:
        TypeError: json_queue not an array of json (key: value) data.
    """
    if not is_json_object(json_queue):
        raise RuntimeError("Expect json_queue to be of dict|list|list[dict] type")
    if not json_queue:
        # Clear queue from file
        with do_open(filename, "w", encoding="utf-8"):
            pass  # Do nothing, empty the file
    else:
        with do_open(filename, "w", encoding="utf-8") as json_file:
            json.dump(json_queue[start:end], json_file, indent=4, separators=(",", ": "))


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
        dict|None: JSON payload with or without timestamp for thingsboard. \
            Returns None if no data was attempted to be packaged.
    """
    if not data:
        return None

    if not ts is None and not isinstance(ts, (int, float, long)):
        raise TypeError("Expect ts to be of numeric type, received %s" % type(ts))

    if isinstance(data, dict):
        if ts is None:
            return data
        return {"ts": ts, "values": data}
    if is_json_string(data) == MQTTHELPER_JSON_DICT:
        if ts is None:
            return json.loads(data)
        return {"ts": ts, "values": json.loads(data)}
    raise ValueError("JSON data format is invalid.")


def publish_mqtt_queue(client, topic, json_queue,
                       timeout=1.0, fifo=True, debug=False):
    """
    paho.mqtt.client.publish() helper to publish json payload with a qos=1 from
    a queue.
    Calling publish_mqtt_queue will modify json_queue.

    Args:
        client (paho.mqtt.client.Client): MQTT Client
        topic (str): MQTT Topic to publish to
        json_queue (list[dict]): JSON array queue for publishing, will be modified.
        timeout (float|int, optional): Timeout to wait for publish ack in \
                                       seconds. Defaults to 1.0.
        fifo (bool, optional): Declare behavior of queue, \
                               True (FIFO), FALSE (FILO). Defaults to True.
        debug (bool, optional): Flag to print each payload being published. \
                                Defaults to False.

    Raises:
        RuntimeError: General exception.

    Returns:
        paho.mqtt.client.MQTTMessageInfo: Publish result
    """
    # No need to publish anything if queue is empty
    if not json_queue:
        return paho.mqtt.client.MQTTMessageInfo(0)
    timeout = max(timeout, 1.0)

    # Initializing baseline values
    json_data_remain = subset_count = len(json_queue)
    json_start = None
    json_end = None

    # Check size of payload to be published and set publishing group
    while (len(json.dumps(json_queue[json_start:json_end]).encode("utf-8"))
            >= MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE):
        # Split payload in half until it fits
        subset_count = subset_count >> 1

        # Unable to find a payload size that fits
        if subset_count == 0:
            raise RuntimeError(paho.mqtt.client.error_string(
                    paho.mqtt.client.MQTT_ERR_PAYLOAD_SIZE))

        # Set correct index for subset group
        if fifo:
            json_end = subset_count
        else:
            json_start = -subset_count
    if debug:
        print("Subset_Count: {0} of {1} ({2})".format(subset_count, json_data_remain,
                                                    "FIFO" if fifo else "FILO"))

    # Loop through json data for publishing
    while json_queue:
        publish_success = False
        try:
            # Result is in tuple (rc, mid) of MQTTMessageInfo class
            publish_result = client.publish(topic=topic,
                                            payload=json.dumps(json_queue[json_start:json_end]),
                                            qos=1)
            # publish_result = paho.mqtt.client.MQTTMessageInfo
            publish_result.wait_for_publish(timeout=timeout)

            if debug:
                print("{0} Size: {1} [{2} of {3}]" \
                        .format(publish_result,
                                len(json.dumps(json_queue[json_start:json_end]).encode("utf-8")),
                                subset_count,
                                json_data_remain
                        )
                )
            # if debug:
            #     print("{0} {1}".format(publish_result, json_queue[json_start:json_end]))
            # if publish_result.rc != paho.mqtt.client.MQTT_ERR_SUCCESS \
            #         or not publish_result._published:
            #     break # Escape publishing loop on publish failure
            if not publish_result.is_published():
                break  # Escape publishing loop on publish failure

        except (ValueError, RuntimeError) as error:
            print("PayloadIndex: [{0},{1}] {2} {3}".format(
                    json_start, json_end, type(error), error))
            break  # Escape loop on error
        except Exception as error:
            print("MQTT Publish Error! PayloadIndex: [{0},{1}] {2} {3}".format(
                    json_start, json_end, type(error), error))
            # break # Escape loop on error
            raise  # Reraise error, unfortunately does not save to file queue
        else:
            publish_success = True
            json_data_remain = max(json_data_remain - subset_count, 0)
            del json_queue[json_start:json_end]

    # Test for edge case where published failed and info.rc returns success
    try:
        if (not publish_success \
                and publish_result.rc == paho.mqtt.client.MQTT_ERR_SUCCESS):
            # publish_result.rc = paho.mqtt.client.MQTT_ERR_UNKNOWN
            publish_result.rc = MQTTHELPER_ERR_EDGE
    except NameError:
        # publish_success = False
        publish_result = paho.mqtt.client.MQTTMessageInfo(0)
        publish_result.rc = paho.mqtt.client.MQTT_ERR_AGAIN

    return publish_result


def publish_to_thingsboard(client, payload, ts=None,
                           fifo=False,
                           timeout=3.0,
                           filename=None,
                           display_payload=False,
                           debug=False):
    """
    paho.mqtt.client.publish() helper to publish to thingsboard using
    publish_mqtt_queue() helper function
    Implements payload archiving queue.

    Args:
        client (paho.mqtt.client.Client()): MQTT client
        payload (dict): JSON payload for appending to queue
        ts (int, optional): Timestamp in milliseconds from epoch. \
            Default - None, ommits timestamp
        fifo (bool, optional):  Declare behavior of queue, \
            True (FIFO), False (FILO). Defaults to False.
        timeout (float, optional): Timeout to wait for publish ack in seconds. \
            Defaults to 3.0.
        filename (str, optional): _description_. Defaults to None.
        display_payload (bool, optional): Name of JSON queue file archive, \
            must include extension in filename. Defaults to False.
        debug (bool, optional): Flag to print each payload being published. \
            Defaults to False.

    Raises:
        ValueError: Invalid payload format.
        TypeError: Timestamp not of numeric type.

    Returns:
        paho.mqtt.client.MQTTMessageInfo: Publish result
    """
    json_filename = generate_filename(filename=filename)

    # Read backup JSON data queue from previous failed uploads
    json_queue = load_queue_from_file(filename=json_filename)
    file_queue_size = len(json_queue)

    current_json_data = package_thingsboard_payload(data=payload, ts=ts)
    if current_json_data:
        if display_payload:
            print(json.dumps(current_json_data))
        append_payload_to_queue(json_queue=json_queue, payload=current_json_data)

    publish_result = publish_mqtt_queue(
        client=client,
        topic="v1/devices/me/telemetry",
        json_queue=json_queue,
        timeout=timeout,
        fifo=fifo,
        debug=debug
    )

    if json_queue or file_queue_size:
        save_queue_to_file(filename=json_filename, json_queue=json_queue)
    return publish_result
