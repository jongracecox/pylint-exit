#!/usr/bin/python
import os
import re
from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Attempt to get version number from TravisCI environment variable
version = os.environ.get('TRAVIS_TAG', default='0.0.0')

# Remove leading 'v'
version = re.sub('^v', '', version)

setup(
    name='pylint-exit',
    description='Exit code handler for pylint command line utility.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version,
    author='Jon Grace-Cox',
    author_email='jongracecox@gmail.com',
    py_modules=['pylint_exit'],
    setup_requires=['setuptools', 'wheel', 'm2r'],
    tests_require=[],
    install_requires=[],
    data_files=[],
    options={
        'bdist_wheel': {'universal': True}
    },
    url='https://github.com/jongracecox/pylint-exit',
    entry_points={
        'console_scripts': ['pylint-exit=pylint_exit:main'],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ]
)
