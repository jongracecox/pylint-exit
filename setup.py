#!/usr/bin/python

import mister_bump
from setuptools import setup

setup(
    name='pylint-exit',
    description='Exit code handler for pylint command line utility.',
    version=mister_bump.bump(style='rc'),
    author='Jon Grace-Cox',
    author_email='jongracecox@gmail.com',
    py_modules=['pylint_exit'],
    setup_requires=['setuptools', 'wheel'],
    tests_require=[],
    install_requires=['bitarray'],
    data_files=[],
    options={
        'bdist_wheel': {'universal': True}
    },
    url='https://github.com/jongracecox/pylint-exit',
    entry_points={
        'console_scripts': ['pylint-exit=pylint_exit:main'],
    }
)
