# mqtthelper: paho.mqtt.client Helper module

This is an MQTT client publishing python helper module.
Contains support and wrapper functions for MQTT publishing.

> [!IMPORTANT]
> **Package is NOT distributed on PyPi package indexer!**

## Dependencies

- paho-mqtt : paho.mqtt.client

## Usage

For IntelliSense support, it is recommended to use one of the following installation options:

1. [Editable](#editable-installation)
2. [Regular](#regular-installation)

Non-Installation use is also possible but provides no IntelliSense support. See [No-Install Usage](#no-installation-example).

### Initial Setup

1. Obtain copy of pyduino files.\
   If Git is installed and you do not want a copy of pyduino files.
   See [Installation from Git Repository](#installation-from-git-repository)\
   If git repo method is used, you can skip the following methods.
2. Traverse to pyduino, python library directory `...\pyduino\python\lib\`.
3. Install package using [regular](#regular-installation) or [editable](#editable-installation) Installation methods.
    Alternatively can ignore installation see [No Installation](#no-installation).

#### Editable Installation

Allows module changes to be automatically updated in the python environment.\
However any package file directory changes will also affect the python environment.

Note: package version does not update automatically, need to perform reinstallation.

```shell
pip install -e ./mqtthelper
```

or

```shell
# if you are in the package directory
# ...\pyduino\python\lib\mqtthelper
pip install -e .
```

#### Regular Installation

Will install the package normally such that any modifications to the package
files is not reflected in the python environment.

Any changes to the packages need to be reinstalled to take effect.

```shell
# `pip install PackageName` will not work as the package is not published in PyPi package indexer.
# Need to traverse into `...\pyduino\python\lib` directory prior to running following command.
pip install ./mqtthelper
```

or

```shell
# if you are in the package directory
# ...\pyduino\python\lib\mqtthelper
pip install -e .
```

##### Installation from Git Repository

This method requires git to be installed on the system and performs a [*regular package installation*](#regular-installation)
directly from the repository without copying all the pyduino files.\
It is NOT recommended to perform an editable mode install from the remote git repo.

```shell
pip install "git+https://github.com/hydrogeologger/pyduino.git#egg=mqtthelper&subdirectory=python/lib/mqtthelper"
```

### No installation

You may choose to not install. However installation offers IntelliSense support.\
See [No-Install Usage](#no-installation-example) to learn how to use the package in python scripts if the package is not installed.

### Example

```python
import time

import paho.mqtt.client as mqtt

import mqtthelper

client = mqtt.Client()
# Using access token,
client.username_pw_set(username="access token")
# Or Using username password, not to be used with publish_to_thingsboard()
client.username_pw_set(username="username", password="password")
client.connect(host="host", port=1883, keepalive=60)

time_since_epoch_millis = time.time() * 1000

data = {
  "temp": 24.0,
  "humidity": 50
}

# Need client loop before publish or else publish will think it always fail due to QOS=1.
client.loop_start()

try:
    # publish_result is in tuple (rc, mid) of MQTTMessageInfo class
    publish_result, _ = mqtthelper.publish_to_thingsboard(
        client=client,
        payload=data,
        ts=time_since_epoch_millis,
        fifo=False,
        timeout=3.0,
        filename="mqtt_queue_demo.json",
        debug=False
    )
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
