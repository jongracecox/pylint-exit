#!/usr/bin/python
import mister_bump
from setuptools import setup
from m2r import parse_from_file
import restructuredtext_lint


# Parser README.md into reStructuredText format
rst_readme = parse_from_file('README.md')

# Validate the README, checking for errors
errors = restructuredtext_lint.lint(rst_readme)

# Raise an exception for any errors found
if errors:
    print(rst_readme)
    raise ValueError('README.md contains errors: ',
                     ', '.join([e.message for e in errors]))

setup(
    name='pylint-exit',
    description='Exit code handler for pylint command line utility.',
    long_description=rst_readme,
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
