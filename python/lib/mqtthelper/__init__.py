#!/usr/bin/env python
"""
This is an MQTT client publishing helper module. Contains support and wrapper
functions for MQTT publishing.

Dependencies:
future
paho.mqtt.client
json
"""

## Python 2/3 compatibility imports
# To print multiple strings, import print_function to prevent Py2 from interpreting it as a tuple:
# from __future__ import print_function
# from builtins import int # subclass of long on Py2
import sys
if sys.version_info >= (3,0):
    long = int

# Module Info
__version__ = "1.0"
__all__ = [
    "is_json_string", "publish_mqtt_queue", "publish_to_thingsboard"
]

# Standard Imports
import os
import json
import paho.mqtt.client
# import __main__ as main
import __main__

# def is_json(text: str) -> bool:
def is_json_string(text):
    """
    Checks if string contains json document.
    Does not check if json document has valid structure.

    Args:
        text: String to test for json document

    Returns:
        True/False for string containing json document
    """
    # Python2 Support for json parsing
    # try:
    #     json.decoder.JSONDecodeError
    # except AttributeError:  # Python 2
    #     json.decoder.JSONDecodeError = ValueError

    if not isinstance(text, (str, bytes, bytearray)):
        return False
    if not text:
        return False
    text = text.strip()
    if text:
        if text[0] in {'{', '['} and text[-1] in {'}', ']'}:
            try:
                json.loads(text)
            except (ValueError, TypeError, json.decoder.JSONDecodeError):
                return False
            else:
                return True
        else:
            return False
    return False

# def publish_mqtt_queue(client: paho.mqtt.client, topic: str, json_payload: json doc,
#                       timeout: float, filename: str | None = None, debug=False) -> paho.mqtt.client.MQTTMessageInfo:
def publish_mqtt_queue(client, topic, json_payload, timeout=1.0,
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
        filename: (Optional) Name of JSON queue file archive, must include extension in filename, Default - None
        debug: (Optional) Flag to print each payload being published, Default - False

    Returns:
        paho.mqtt.client.MQTTMessageInfo of paho.mqtt.client.publish call

    Raises:
        ValueError: Invalid payload format.
    """
    if timeout <= 1.0:
        timeout = 1.0

    if filename is not None:
        json_filename = filename.strip()
    if filename is None or filename == "":
        # parent_filename = os.path.basename(main.__file__).rsplit('.', 1)[0]
        parent_filename = os.path.basename(__main__.__file__).rsplit('.', 1)[0]
        json_filename = "mqtt_queue_%s.json" % parent_filename

    # Read backup JSON Data from previous failed uploads
    json_data = []
    if os.path.isfile(json_filename):
        with open(json_filename) as json_file:
            try:
                json_data = json.load(json_file)
            except ValueError:
                pass # JSON file is empty

    # try:
    if isinstance(json_payload, (dict, list)):
        json_data.append(json_payload)
    elif is_json_string(json_payload):
        json_data.append(json.loads(json_payload))
    else:
        raise ValueError("json payload format is invalid.")
    # except ValueError:
    #     raise ValueError("json payload format is invalid.")

    # Loop through json data for publishing
    payload_index = 0
    for payload_index, index_json_payload in enumerate(json_data):
        publish_success = False
        try:
            # Result is in tuple (rc, mid) of MQTTMessageInfo class
            publish_result = client.publish(topic=topic, payload=json.dumps(index_json_payload), qos=1)
            # publish_result = paho.mqtt.client.MQTTMessageInfo
            publish_result.wait_for_publish(timeout=timeout)
            if debug:
                print("{0} {1}".format(publish_result, index_json_payload))
            # if publish_result.rc != paho.mqtt.client.MQTT_ERR_SUCCESS or not publish_result._published:
            #     break # Escape publishing loop on publish failure
            if not publish_result.is_published():
                break # Escape publishing loop on publish failure
        except (ValueError, RuntimeError) as error:
            print("PayloadIndex: {0} {1} {2}".format(payload_index, type(error), error))
            break # Escape loop on error
        except Exception as error:
            print("MQTT Publish Error! PayloadIndex: {0} {1} {2}".format(payload_index, type(error), error))
            break # Escape loop on error
        else:
            publish_success = True

    # Test for edge case where published failed and info.rc returns success
    try:
        if not publish_success and publish_result.rc == paho.mqtt.client.MQTT_ERR_SUCCESS:
            publish_result.rc = paho.mqtt.client.MQTT_ERR_UNKNOWN
    except NameError:
        # publish_success = False
        publish_result = paho.mqtt.client.MQTTMessageInfo(payload_index)
        publish_result.rc = paho.mqtt.client.MQTT_ERR_UNKNOWN

    # If payload index and publish_result.mid does not match then there was a failure in publishing
    len_json_data = len(json_data)
    if publish_success and len_json_data > 1 and (payload_index + 1) == len_json_data:
        # Clear the queue as all payloads was successfully published
        with open(json_filename, 'w') as json_file:
            # Do nothing, empty the file
            pass
    elif not publish_success:
        # Archive unsent data to file queue for sending later
        with open(json_filename, 'w') as json_file:
            json.dump(json_data[payload_index:], json_file, indent=4, separators=(",", ": "))

    # If payload index and publish_result.mid does not match then there was a failure in publishing
    # if publish_result.rc != paho.mqtt.client.MQTT_ERR_SUCCESS:
    #     # Archive unsent data to file queue for sending later
    #     with open(json_filename, 'w') as json_file:
    #         json.dump(json_data[payload_index:], json_file, indent=4, separators=(",", ": "))
    # elif (publish_result.rc == paho.mqtt.client.MQTT_ERR_SUCCESS and \
    #         len(json_data) > 1 and \
    #         (payload_index + 1) == len(json_data)):
    #     # Clear the queue as all payloads was successfully published
    #     with open(json_filename, 'w') as json_file:
    #         # Do nothing, empty the file
    #         pass

    # if publish_result.is_published():
    #     if len(json_data) > 1 and (payload_index + 1) == len(json_data):
    #         with open(json_filename, 'w') as json_file:
    #             pass #empty the file
    # else:
    #     # Archive unsent data to file queue for sending later
    #     with open(json_filename, 'w') as json_file:
    #         json.dump(json_data[payload_index:], json_file, indent=4, separators=(",", ": "))

    return publish_result

# publish_to_thingsboard: (client: paho.mqtt.client.Client(), payload: str,
#                           ts: int | None = None, timeout: float = 1,
#                           filename: str | None = None, display_payload: bool = False,
#                           debug: bool = False) -> paho.mqtt.client.MQTTMessageInfo:
def publish_to_thingsboard(client, payload, ts=None,
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
        filename: (Optional) Name of JSON queue file archive, must include extension in filename, Default - None
        display_payload: (Optional) Displays the current payload to be appended, Default - False
        debug: (Optional) Flag to print each payload being published, Default - False

    Returns:
        paho.mqtt.client.MQTTMessageInfo of paho.mqtt.client.publish call

    Raises:
        ValueError: Invalid payload format.
        TypeError: Timestamp not of numeric type.
    """
    if ts is None:
        current_json_data = payload
    elif not isinstance(ts, (int, float, long)):
        raise TypeError("Expect ts to be of numeric type, received %s" % type(ts))
    else:
        if isinstance(payload, (dict, list)):
            current_json_data = {"ts":ts, "values": payload}
        elif is_json_string(payload):
            current_json_data = {"ts":ts, "values": json.loads(payload)}
        else:
            raise ValueError("json payload format is invalid.")
    
    if display_payload:
        print(current_json_data)

    publish_result = publish_mqtt_queue(client=client, topic="v1/devices/me/telemetry",
            json_payload=current_json_data, timeout=timeout,
            filename=filename, debug=debug)
    return publish_result


# def publish_thingsboard(client, json_filename, milliseconds_since_epoch, data_collected,
#                         screen_display=True, debug=False):
#     '''
#     paho.mqtt.client publish to thingsboard wrapper with data queue.
#     '''
#     from os import path
#     import json
#     import paho.mqtt.client as mqtt

#     # JSON_FILENAME = "tsqueue_ewatering_sa1.json"
#     json_data = []

#     # Create JSON data with time stamp
#     current_json_data = {"ts":milliseconds_since_epoch, "values": data_collected}
#     # json_data = data_collected
#     if debug:
#         print(current_json_data)

#     # Read backup JSON Data from previous failed uploads
#     if path.isfile(json_filename):
#         with open(json_filename) as json_file:
#             try:
#                 json_data = json.load(json_file)
#             except ValueError:
#                 pass # Empty json file

#     json_data.append(current_json_data)

#     # Loop through json data for publishing
#     payload_index = 0
#     for payload_index, json_payload in enumerate(json_data):
#         try:
#             # Result is in tuple (rc, mid) of MQTTMessageInfo class
#             publish_result = client.publish(topic='v1/devices/me/telemetry', payload=json.dumps(json_payload), qos=1)
#         except (ValueError, RuntimeError) as error:
#             if screen_display:
#                 print "PayloadIndex:", payload_index, type(error), error
#                 break # Escape loop on error
#         except Exception as error:
#             print "TS Publish Error! PayloadIndex:", payload_index, type(error), error
#             break # Escape loop on error

#         # if debug:
#         #     print publish_result, json_payload
#         if publish_result.rc != mqtt.MQTT_ERR_SUCCESS:
#             break # Escape publishing loop on publish failure

#     # If payload index and publish_result.mid does not match then there was a failure in publishing
#     if publish_result.rc != mqtt.MQTT_ERR_SUCCESS:
#         # Archive data to send later
#         with open(json_filename, 'w') as json_file:
#             json.dump(json_data[payload_index:], json_file, indent=4, separators=(",", ": "))
#     elif (publish_result.rc == mqtt.MQTT_ERR_SUCCESS and \
#             len(json_data) > 1 and \
#             (payload_index + 1) == len(json_data)):
#         with open(json_filename, 'w') as json_file:
#             pass #empty the file

#     # Tidy up publishing memory use
#     json_data = []

#     if screen_display:
#         print(publish_result) # Display the last publish result
#     return publish_result