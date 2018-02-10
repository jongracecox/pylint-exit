#!/usr/bin/python
import mister_bump
from setuptools import setup
from m2r import parse_from_file

setup(
    name='pylint-exit',
    description='Exit code handler for pylint command line utility.',
    long_description=parse_from_file('README.md'),
    version=mister_bump.bump(style='rc'),
    author='Jon Grace-Cox',
    author_email='jongracecox@gmail.com',
    py_modules=['pylint_exit'],
    setup_requires=['setuptools', 'wheel', 'm2r'],
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
