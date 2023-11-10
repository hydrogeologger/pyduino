#!/usr/bin/env python
import os.path
import codecs
from setuptools import setup

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

if __name__ == "__main__":
    setup(
        version = get_version(os.path.join("mqtthelper", "__init__.py")),
        # install_requires = [
            # "paho-mqtt >= 1.6.1"
        # ]
    )
