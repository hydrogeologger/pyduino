"""
This is an MQTT client publishing helper module providing file base queue redundancy support.

Contains support and wrapper functions for MQTT publishing and publishing to
thingsboard.

Dependencies:
- paho-mqtt : paho.mqtt.client
"""
# Python 2/3 compatilibity standard imports
# from builtins import int, open
# pylint: disable=consider-using-f-string # Hide warning for python 2 support

# Module Info
__version__ = "1.1.0"
__all__ = [
    "generate_queue_filepath",
    "is_json_object",
    "is_json_string",
    "load_queue_from_file",
    "append_payload_to_queue",
    "save_queue_to_file",
    "package_thingsboard_payload",
    "publish_mqtt_queue",
    "publish_to_thingsboard"
]

# To print multiple strings, import print_function to prevent Py2 from interpreting it as a tuple:
# from __future__ import print_function  # Allow encoding parameter in open()

# Standard Imports
import json as _json
import os as _os
import sys as _sys
from typing import IO as _IO
from typing import Any as _Any

# Third Party Imports
import paho.mqtt.client as _mqtt_client

# Package imports
try:
    from __main__ import __file__ as _main_script_path
except ImportError:
    # Just in case module was not imported via a file
    from __main__ import __name__ as _main_script_path


# Python 2/3 Compatibility Support
# The long builtin no longer exists in Python3.
if _sys.version_info[0] >= 3:
    long = int  # pylint: disable=invalid-name


def _do_open(file, mode, encoding, *args, **kwargs):
    # type: (str|bytes|_os.PathLike, str, str|None, ..., ...) -> _IO
    """Wrapper for builtin python open() compatibility between python2 and python3.
    Removes encoding argument from open() for python2

    Args:
        file (FileDescriptorOrPath): File descriptor or path.
        mode (str): File open mode.
        encoding (str): open method encoding.

    Returns:
        File object.
    """
    if _sys.version_info.major >= 3:
        return open(file, mode, *args, encoding=encoding, **kwargs)
    if "encoding" in kwargs:
        del kwargs["encoding"]
    return open(file, mode, *args, **kwargs)  # pylint: disable=unspecified-encoding


# Globals
# As per NETTY_MAX_PAYLOAD_SIZE from MQTT Broker/Thingsboard
MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE = 65536
"""As per MQTT Broker MAX Payload Bytes Size Setting."""


# Error Code
MQTTHELPER_ERR_INVALID = 0
"""MQTTHELPER Error - General Invalid Error Number."""
MQTTHELPER_ERR_EDGE = -2
"""MQTTHELPER Error - Edge Case Error Number."""

# JSON Type
MQTTHELPER_JSON_DICT = 1
"""MQTTHELPER JSON Type - Dictionary."""
MQTTHELPER_JSON_ARRAY = 2
"""MQTTHELPER JSON Type - Dictionary List."""


def generate_queue_filepath(filepath=None):
    # type: (str|None) -> str
    """Generate the file path for queue storage.

    Args:
        filepath (str, optional): File path including file extension. Defaults to None.

    Returns:
        str: File path including extension. i.e absolute/path/to/mqtt_queue_callingscriptname.json.
    """
    if filepath is not None:
        filepath = filepath.strip()
    if filepath is None or filepath == "":
        script_name = _os.path.splitext(
            _os.path.basename(_main_script_path))[0]
        filepath = _os.path.join(
            _os.path.dirname(_os.path.abspath(_main_script_path)),
            "mqtt_queue_%s.json" % script_name)
    return filepath


def is_json_object(object_):
    # type: (_Any) -> int
    """Check if object is of type dictionary or list of dictionary.

    Args:
        object_ (any): Python object.

    Returns:
        int: Literal value representing valid json object.

            - Invalid - 0, MQTTHELPER_ERR_INVALID.
            - Dict - 1, MQTTHELPER_JSON_DICT.
            - List of dictionary - 2, MQTTHELPER_JSON_ARRAY.
    """
    if isinstance(object_, dict):
        return MQTTHELPER_JSON_DICT
    if (isinstance(object_, list) and all(isinstance(item, dict) for item in object_)):
        return MQTTHELPER_JSON_ARRAY
    return MQTTHELPER_ERR_INVALID


def is_json_string(text):
    # type: (str) -> int
    """Checks if string contains json document.

    Does not check if json document has valid structure.

    Args:
        text (str): String to test for json document.

    Returns:
        int: Literal value representing valid json string.

            - Invalid - 0, MQTTHELPER_ERR_INVALID.
            - Dict - 1, MQTTHELPER_JSON_DICT.
            - List of dictionary - 2, MQTTHELPER_JSON_ARRAY.
    """
    if not text or not isinstance(text, (str, bytes, bytearray)):
        return MQTTHELPER_ERR_INVALID
    text = text.strip()
    if text and (text[0] in {'{', '['} and text[-1] in {'}', ']'}):
        try:
            return (is_json_object(_json.loads(text)))
        except (ValueError, TypeError):
            # json.decoder.JSONDecodeError inherits from ValueError
            return MQTTHELPER_ERR_INVALID
    return MQTTHELPER_ERR_INVALID


def load_queue_from_file(filepath):
    # type (str) -> list[dict]
    """Load json queue from file.

    Args:
        filepath (str): File path containing json queue.

    Returns:
        list[dict]: JSON array.
    """
    # Read backup JSON Data from previous failed uploads
    if _os.path.isfile(filepath):
        with _do_open(filepath, "r", encoding='utf-8') as json_file:
            try:
                json_queue = _json.load(json_file)
                if isinstance(json_queue, dict):
                    return [json_queue]
                return json_queue
                # json_data_payload_size = len(_json.dumps(json_data).encode("utf-8"))
            except ValueError:
                pass  # JSON file is empty
    return []


def append_payload_to_queue(payload, json_queue):
    # type: (dict|list[dict]|str, list[dict]) -> None
    """Append json object to queue, modifies json_queue.

    Args:
        payload (dict | list[dict] | str): JSON object to append to queue.
        queue (list): List containing json data.

    Raises:
        ValueError: If payload format is not dict, list[dict] or json string format.
    """
    json_type = is_json_object(payload)
    if json_type == MQTTHELPER_JSON_DICT:
        json_queue.append(payload)
    elif json_type == MQTTHELPER_JSON_ARRAY:
        # Expect a list of dictionary items
        json_queue.extend(payload)
    else:
        json_type = is_json_string(payload)
        if json_type == MQTTHELPER_JSON_DICT:
            json_queue.append(_json.loads(payload))
        elif json_type == MQTTHELPER_JSON_ARRAY:
            # Expect a list of dictionary items
            json_queue.extend(_json.loads(payload))
        else:
            raise ValueError("json payload format is invalid.")


# def save_json_mqtt_queue(filename, json_data, payload_index=None):
def save_queue_to_file(filepath, json_queue, start=None, end=None):
    # type: (str, list, int|None, int|None) -> None
    """Saves json mqtt queue to file.

    Args:
        filename (str): Name of JSON queue file archive, must include
            extension in filename.
        json_queue (list): List of json data.
        start (int, optional): List index to start saving from.. Defaults to None.
        end (int, optional): List index end to save to. Defaults to None.

    Raises:
        TypeError: json_queue not an array of json (key: value) data.
    """
    if not is_json_object(json_queue):
        raise RuntimeError(
            "Expect json_queue to be of dict|list|list[dict] type")
    if not json_queue:
        # Clear queue from file
        with _do_open(filepath, "w", encoding="utf-8"):
            pass  # Do nothing, empty the file
    else:
        with _do_open(filepath, "w", encoding="utf-8") as json_file:
            _json.dump(json_queue[start:end], json_file,
                       indent=4, separators=(",", ": "))


def publish_mqtt_queue(client, topic, json_queue,
                       timeout=1.0, fifo=False, debug=False,
                       max_payload_bytes=MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE):
    # type: (_mqtt_client.Client, str, list[dict], int|float, bool|None, bool|None, int) -> _mqtt_client.MQTTMessageInfo # pylint: disable=line-too-long
    """paho.mqtt.client.publish() helper to publish json payload from queue.

    Publishing is performed with qos=1.
    Calling publish_mqtt_queue will modify json_queue.

    Args:
        client (Client): MQTT Client.
        topic (str): MQTT Topic to publish to.
        json_queue (list[dict]): JSON array queue for publishing, will be modified.
        timeout (float|int, optional): Timeout to wait for publish ack in
            seconds. Defaults to 1.0.
        fifo (bool, optional): Declare behavior of queue,
            True (FIFO), FALSE (LIFO). Defaults to False.
        debug (bool, optional): Flag to print each payload being published.
            Defaults to False.
        max_payload_bytes (int, optional): Max size of payload per transmit cycle.
            Defaults to MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE.

    Raises:
        RuntimeError: General exception.

    Returns:
        paho.mqtt.client.MQTTMessageInfo: Iterable object that contains information about the published message.
            Such that (rc, mid) = client.publish(...) is still valid.
            - mid (int): The message ID.
            - rc (int): The result code of the publish call.
    """
    # No need to publish anything if queue is empty
    if not json_queue:
        return _mqtt_client.MQTTMessageInfo(0)
    timeout = max(timeout, 1.0)

    # Initializing baseline values
    json_data_remain = subset_count = len(json_queue)
    json_start = None
    json_end = None

    # Check size of payload to be published and set publishing group
    while (len(_json.dumps(json_queue[json_start:json_end]).encode("utf-8")) >= max_payload_bytes):
        # Split payload in half until it fits
        subset_count = subset_count >> 1

        # Unable to find a payload size that fits
        if subset_count == 0:
            raise RuntimeError(_mqtt_client.error_string(
                _mqtt_client.MQTT_ERR_PAYLOAD_SIZE))

        # Set correct index for subset group
        if fifo:
            json_end = subset_count
        else:
            json_start = -subset_count
    if debug:
        print("Subset_Count: {0} of {1} ({2})".format(subset_count, json_data_remain,
                                                      "FIFO" if fifo else "LIFO"))

    # Loop through json data for publishing
    while json_queue:
        publish_success = False
        try:
            # Result is in tuple (rc, mid) of MQTTMessageInfo class
            publish_result = client.publish(topic=topic,
                                            payload=_json.dumps(
                                                json_queue[json_start:json_end]),
                                            qos=1)
            # publish_result = paho.mqtt.client.MQTTMessageInfo
            publish_result.wait_for_publish(timeout=timeout)

            if debug:
                print("{0} Size: {1} [{2} of {3}]"
                      .format(publish_result,
                              len(_json.dumps(
                                  json_queue[json_start:json_end]).encode("utf-8")),
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
            print("PayloadIndex: [{0},{1}] of {2}. {3} {4}".format(
                json_start, json_end, json_data_remain, type(error), error))
            break  # Escape loop on error
        except Exception as error:
            print("MQTT Publish Error! PayloadIndex: [{0},{1}] of {2}. {3} {4}".format(
                json_start, json_end, json_data_remain, type(error), error))
            # break # Escape loop on error
            raise  # Reraise error, unfortunately does not save to file queue
        else:
            publish_success = True
            del json_queue[json_start:json_end]
            json_data_remain = max(json_data_remain - subset_count, 0)

    # Test for edge case where published failed and info.rc returns success
    try:
        if (not publish_success and
                publish_result.rc == _mqtt_client.MQTT_ERR_SUCCESS):
            # publish_result.rc = paho.mqtt.client.MQTT_ERR_UNKNOWN
            publish_result.rc = MQTTHELPER_ERR_EDGE
    except NameError:
        # publish_success = False
        publish_result = _mqtt_client.MQTTMessageInfo(0)
        publish_result.rc = _mqtt_client.MQTT_ERR_AGAIN

    return publish_result


def package_thingsboard_payload(data, ts=None):
    # type (dict, int|None) -> dict[str, any]|None
    """Prepare payload for thingsboard.

    Args:
        data: JSON data for repackaging.
        ts (int, optional): UTC Timestamp in milliseconds since epoch.
            Defaults to None - omits timestamp.

    Raises:
        TypeError: Timestamp not of numeric type.
        ValueError: Invalid payload format.

    Returns:
        dict|None: Returns None if no data was attempted to be packaged.
            Dictionary as per thingsboard JSON object will include:
            If includes timestamp:
            - "ts" (int): Timestamp in milliseconds since epoch.
            - "values" (dict): Dictionary containing key: value pair data.
            If no timestamp: Standard dictionary containing key: value pair data.
    """
    if not data:
        return None

    # pylint: disable-next=possibly-used-before-assignment # use of long for py2 support
    if not ts is None and not isinstance(ts, (int, float, long)):
        raise TypeError(
            "Expect ts to be of numeric type, received %s" % type(ts))

    if isinstance(data, dict):
        if ts is None:
            return data
        return {"ts": ts, "values": data}
    if is_json_string(data) == MQTTHELPER_JSON_DICT:
        if ts is None:
            return _json.loads(data)
        return {"ts": ts, "values": _json.loads(data)}
    raise ValueError("JSON data format is invalid.")


def publish_to_thingsboard(client, payload, ts=None,
                           fifo=False,
                           timeout=3.0,
                           filename=None,
                           debug=False,
                           max_payload_bytes=MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE):
    # type: (_mqtt_client.Client, dict|list[dict]|str, int|None, bool|None, int|float, str|None, bool|None, int) -> tuple[_mqtt_client.MQTTMessageInfo, dict|None] # pylint: disable=line-too-long
    """paho.mqtt.client.publish() helper publishing to thingsboard with payload queueing.

    Implements payload file archiving queue.

    Args:
        client (paho.mqtt.client.Client()): MQTT client
        payload (dict): JSON payload for appending to queue
        ts (int, optional): Timestamp in milliseconds from epoch.
            Default - None, omits timestamp
        fifo (bool, optional):  Declare behavior of queue,
            True (FIFO), False (LIFO). Defaults to False.
        timeout (float, optional): Timeout to wait for publish ack in seconds.
            Defaults to 3.0.
        filepath (str, optional): Name of JSON queue file archive file path,
            must include extension in filename/path. Defaults to None.
        debug (bool, optional): Flag to print each payload being published.
            Defaults to False.
        max_payload_bytes (int, optional): Max size of payload per transmit cycle.
            Defaults to MQTTHELPER_NETTY_MAX_PAYLOAD_SIZE.

    Raises:
        ValueError: Invalid payload format.
        TypeError: Timestamp not of numeric type.

    Returns:
        tuple[MQTTMessageInfo,dict|None]: A tuple containing:
            - paho.mqtt.client.MQTTMessageInfo: Iterable object that contains information about the published message.
                - mid (int): The message ID.
                - rc (int): The result code of the publish call.
            - dict | None: Dictionary of constructed payload or None if payload is empty.
    """
    json_filepath = generate_queue_filepath(filepath=filename)

    # Read backup JSON data queue from previous failed uploads
    json_queue = load_queue_from_file(filepath=json_filepath)
    file_queue_size = len(json_queue)

    current_json_data = package_thingsboard_payload(data=payload, ts=ts)
    if current_json_data:
        append_payload_to_queue(json_queue=json_queue,
                                payload=current_json_data)

    publish_result = publish_mqtt_queue(
        client=client,
        topic="v1/devices/me/telemetry",
        json_queue=json_queue,
        timeout=timeout,
        fifo=fifo,
        debug=debug,
        max_payload_bytes=max_payload_bytes
    )

    if json_queue or file_queue_size:
        save_queue_to_file(filepath=json_filepath, json_queue=json_queue)
    return (publish_result, current_json_data)
