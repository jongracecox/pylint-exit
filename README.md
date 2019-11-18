# pylint-exit

[![pypi package](https://badge.fury.io/py/pylint-exit.svg)](https://pypi.org/project/pylint-exit)
[![build status](https://api.travis-ci.org/jongracecox/pylint-exit.svg?branch=master)](https://travis-ci.org/jongracecox/pylint-exit)
[![downloads](https://img.shields.io/pypi/dm/pylint-exit.svg)](https://pypistats.org/packages/pylint-exit)
[![GitHub last commit](https://img.shields.io/github/last-commit/jongracecox/pylint-exit.svg)](https://github.com/jongracecox/pylint-exit/commits/master)
[![GitHub](https://img.shields.io/github/license/jongracecox/pylint-exit.svg)](https://github.com/jongracecox/pylint-exit/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jongracecox/pylint-exit.svg?style=social)](https://github.com/jongracecox/pylint-exit/stargazers)

Utility to handle pylint exit codes on Linux in a scripting-friendly way.

Pylint uses bit-encoded exit codes to convey the results of the pylint review,
which means it will return with a non-zero return code even when the
pylint scoring was successful.

This can make it difficult to script the execution of pylint while at the same time
detecting genuine errors.

`pylint-exit` is a small command-line utility that can be used to re-process
the pylint return code and translate it into a scripting-friendly return code.

`pylint-exit` will decode the bit-encoded return code, identify whether there were
any fatal messages issued (which might constitute a failure in the execution of
pylint), or a usage error, and return a `0` or `1` return code that is more easily
used in shell scripts.

# Installation

The simplest way to install is via `pip`.

```bash
pip install pylint-exit
```

This will install the package, and will provide the `pylint-exit` command line utility.

You can also manually install by downloading `pylint_exit.py`, and make it executable.

```bash
curl -o pylint-exit https://raw.githubusercontent.com/jongracecox/pylint-exit/master/pylint_exit.py && chmod +x pylint_exit.py
```

You should also consider creating a symbolic link so that the calls in the remainder of this
README work as described.  Update `<path-to>` with where you downloaded the script.

```bash
ln -s <path-to>/pylint_exit.py /usr/local/bin/pylint-exit
```

*Note: If you perform a `--user` install with `pip` then you will need to ensure `~/.local/bin` appears in your `PATH`
environment variable, otherwise the command line `pylint-exit` will not work.* 

# Usage
Add `|| pylint-exit $?` to the end of your existing Pylint command.  You can then
use the updated `$?` return code in your shell script.

```bash
pylint mymodule.py || pylint-exit $?
if [ $? -ne 0 ]; then
  echo "An error occurred while running pylint." >&2
  exit 1
fi
```

Note: Many CI tools will check the return code of each command, so it may be enough to
simply add `|| pylint-exit $?`, and leave the return code check to the CI executor.

You can also use the python code directly if needed:

```bash
pylint mymodule.py || python pylint_exit.py $?
```

# Return codes
Pylint can return combinations of the following codes.  `pylint-exit` will identify each
issued message, and return the maximum final return code.

| Pylint code | Message | Final return code |
| ----------- | ------- | ----------------- |
| 1  | Fatal message issued | 1 |
| 2  | Error message issued | 0 |
| 4  | Warning message issued | 0 |
| 8  | Refactor message issued | 0 |
| 16 | Convention message issued | 0 |
| 32 | Usage error | 1 |

This list is stored in `exit_codes_list`, which can be customised if needed.

You can control what is considered a failure using the following command line arguments.
By default these types of messages don't cause a non-zero return code. Adding
any of these arguments will trigger a non-zero return code when those types of
message are raised. 

| Name | Meaning |
| ---- | ------- |
| `-efail`, `--error-fail` | Fail on issued error messages. |
| `-wfail`, `--warn-fail` | Fail on issued warning messages. |
| `-rfail`, `--refactor-fail` | Fail on issued refactor messages. |
| `-cfail`, `--convention-fail` | Fail on issued convension messages. |

# Examples

## Exiting gracefully on non-severe messages
In this example pylint issues refactor and convention messages, and exits with a
return code of 24.  `pylint-exit` decodes this, displays the messages, and exits
with a return code of 0.

```bash
> pylint --rcfile=.pylintrc --output-format=text mymodule.py || pylint-exit $?
The following messages were raised:

  - refactor message issued
  - convention message issued
 
No fatal messages detected.  Exiting gracefully...
> echo $?
0
```

## Exiting with an error on severe messages
In this example pylint returns with a usage error due to the bad output format, and
exits with a return code of 32.  `pylint-exit` detects this, displays the message, and
returns with an exit code of 1.

```bash
> pylint --rcfile=.pylintrc --output-format=badformat mymodule.py || pylint-exit $?
The following messages were raised:

  - usage error

Fatal messages detected.  Failing...
> echo $?
1
```

## Treating errors and warnings as severe
In this example we will use the `--error-fail` and `--warn-fail` command line arguments
to cause pylint-exit to treat errors and warnings as serious enough to return a non-zero
return code.

In the example scenario pylint issues error and warning messages, and exits with a
return code of 6.  `pylint-exit` decodes this, displays the messages, and exits
with a return code of 1 because the error and warning messages are now considered as
fatal.


```bash
> pylint --rcfile=.pylintrc --output-format=badformat mymodule.py || pylint-exit $?
The following messages were raised:

  - error message issued
  - warning message issued

Fatal messages detected.  Failing...
> echo $?
1

```

# Testing

You can test how pylint-exit will react to various return codes using the following command:

```bash
(exit 6) || pylint-exit $?
```

or if you are using the python code directly:

```bash
(exit 6) || python pylint_exit.py $?
```
