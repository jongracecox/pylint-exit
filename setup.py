#!/usr/bin/python

import sys
import re
from setuptools import setup

def get_version():
    with open("pylint_exit.py", "r") as file_handle:
        file_text = file_handle.read()
    version_match = re.search(r'.* __version__ = [\'"]([^\'"]*)[\'"]', file_text)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to identify version string.")

setup(
    name='pylint-exit',
    description='Exit code handler for pylint command line utility.',
    version=get_version(),
    author='Jon Grace-Cox',
    author_email='jongracecox@gmail.com',
    py_modules = ['pylint_exit'],
    setup_requires=['setuptools', 'wheel'],
    tests_require=[],
    install_requires=['bitarray'],
    data_files=[],
    options={
        'bdist_wheel': {'universal': True}
    },
    url='https://github.com/jongracecox/pylint-exit',
    entry_points = {
        'console_scripts': ['pylint-exit=pylint_exit:main'],
    }
)
