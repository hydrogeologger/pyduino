<!-- markdownlint-disable -->

# API Overview

## Modules

- [`mqtthelper`](./mqtthelper.md#module-mqtthelper): This is an MQTT client publishing helper module providing file base queue redundancy support.
- [`mqtthelper.log`](./mqtthelper.log.md#module-mqtthelperlog): Logging configuration for the package.

## Classes

- No classes

## Functions

- [`mqtthelper.append_payload_to_queue`](./mqtthelper.md#function-append_payload_to_queue): Append json object to queue, modifies json_queue.
- [`mqtthelper.generate_queue_filepath`](./mqtthelper.md#function-generate_queue_filepath): Generate the file path for queue storage.
- [`mqtthelper.is_json_object`](./mqtthelper.md#function-is_json_object): Check if object is of type dictionary or list of dictionary.
- [`mqtthelper.is_json_string`](./mqtthelper.md#function-is_json_string): Checks if string contains json document.
- [`mqtthelper.load_queue_from_file`](./mqtthelper.md#function-load_queue_from_file): Load json queue from file.
- [`mqtthelper.package_thingsboard_payload`](./mqtthelper.md#function-package_thingsboard_payload): Prepare payload for thingsboard.
- [`mqtthelper.publish_mqtt_queue`](./mqtthelper.md#function-publish_mqtt_queue): paho.mqtt.client.publish() helper to publish json payload from queue.
- [`mqtthelper.publish_to_thingsboard`](./mqtthelper.md#function-publish_to_thingsboard): paho.mqtt.client.publish() helper publishing to thingsboard with payload queueing.
- [`mqtthelper.save_queue_to_file`](./mqtthelper.md#function-save_queue_to_file): Saves json mqtt queue to file.
- [`log.configure`](./mqtthelper.log.md#function-configure): Configure the default logging behavior and stream for the library.
- [`log.disable`](./mqtthelper.log.md#function-disable): Disable the default output handler for the library.
- [`log.get_level`](./mqtthelper.log.md#function-get_level): Return the current logging level of the package logger.
- [`log.get_logger`](./mqtthelper.log.md#function-get_logger): Return the primary package logger.
- [`log.set_level`](./mqtthelper.log.md#function-set_level): Directly set the logging level for the package.
