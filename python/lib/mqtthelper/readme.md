# mqtthelper: paho.mqtt.client Helper module

This is an MQTT client publishing python helper module.
Contains support and wrapper functions for MQTT publishing.

NOTE: Package is currently not distributed on PyPi package indexer!

## Dependencies

- paho-mqtt : paho.mqtt.client

## Usage

For IntelliSense support, it is recommended to use one of the following installation options:

1. [editable](#editable-installation)
2. [regular](#regular-installation)

Non-Installation use is also possible but provides no IntelliSense support. See [No-Install Usage](#no-installation-example).

### Initial Setup

1. Obtain copy of pyduino files.\
   If Git is installed and you do not want a copy of pyduino files.
   See [Installation from Git Repository](#installation-from-git-repository)\
   If git repo method is used, you can skip the following methods.
2. Traverse to pyduino, python library directory `pyduino\python\lib\`.
3. Install package using [regular](#regular-installation) or [editable](#editable-installation) Installation methods.
    Alternatively can ignore installation see [No Installation](#no-installation).

#### Editable Installation

Allows module changes to be automatically updated in the python environment.\
However any package file directory changes will also affect the python environment.

Note: package version does not update automatically, need to perform reinstallation.

```bash
pip install -e ./mqtthelper
or
pip install -e . # if you are in the ...\lib\mqtthelper directory
```

#### Regular Installation

Will install the package normally such that any modifications to the package
files is not reflected in the python environment.

Any changes to the packages need to be reinstalled to take effect.

```bash
# `pip install PackageName` will not work as the package is not published in PyPi package indexer.
# Need to traverse into package directory prior to running following command.
pip install ./mqtthelper
or
pip install -e . # if you are in the ...\lib\mqtthelper directory
```

#### Installation from Git Repository

This method requires git to be installed on the system and performs a [*regular package installation*](#regular-installation)
directly from the repository without copying all the pyduino files.

```bash
pip install "git+https://github.com/hydrogeologger/pyduino.git#egg=mqtthelper&subdirectory=python/lib/mqtthelper"
```

### No installation

You may choose to not install. However installation offers IntelliSense support.\
See [No-Install Usage](#no-installation-example) to learn how to use the package in python scripts if the package is not installed.

### Example

```python
import time

import paho.mqtt.client as mqtt

client = mqtt.Client()
# Using username password
client.username_pw_set(username="username", password="password")
# Or using access token
client.username_pw_set(username="access token")
client.connect(host="host", port=1883, keepalive=60)

# Need client loop before publish or else publish will think it always fail due to QOS=1.
client.loop_start()

time_since_epoch_ms = time.time() * 1000

data = {
  "temp": 24.0,
  "humidity": 50
}

try:
    # Result is in tuple (rc, mid) of MQTTMessageInfo class
    publish_result = mqtthelper.publish_to_thingsboard(
            client=client,
            payload=data,
            ts=time_since_epoch_ms,
            fifo=False,
            timeout=3.0,
            filename="mqtt_queue_demo.json",
            display_payload=True,
            debug=False)
except (ValueError, RuntimeError) as error:
    print(error)

if (client.is_connected()):
    client.loop_stop()
    client.disconnect()
```

#### No-Installation Example

Note this method does not provide IntelliSense support! For IntelliSense please use one of the [installation](#initial-setup) methods.

```python
# Need to add path to package module files before importing
sys.path.append("/path/to/pyduino/python/lib/mqtthelper/src")
import mqtthelper
```

## API

See documentation [here](<./docs/readme.md>)
