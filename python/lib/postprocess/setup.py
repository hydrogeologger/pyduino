"""A setuptools based setup module shim.

Required for editable installs.

Notes:
Passing of version into setup() is required for python2.7 due to ast (Abstract syntax tree) module.
https://github.com/pypa/setuptools/pull/1753

Reference:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
https://github.com/pypa/sampleproject
"""
import sys

from setuptools import setup

if sys.version_info < (3, 0):
    import codecs
    import os.path

    def read(rel_path):  # pylint: disable=missing-function-docstring
        here = os.path.abspath(os.path.dirname(__file__))
        with codecs.open(os.path.join(here, rel_path), 'r') as fp:
            return fp.read()

    def get_version(rel_path):  # pylint: disable=missing-function-docstring
        for line in read(rel_path).splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        raise RuntimeError("Unable to find version string.")


if __name__ == "__main__":
    if sys.version_info < (3, 0):
        setup(
            version=get_version(
                os.path.join("src", "postprocess", "__init__.py")
            ),
            # install_requires = [
            # "pandas >= 0.24.2",
            # "requests"
            # ]
        )
    else:
        setup()
