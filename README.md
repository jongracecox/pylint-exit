# pylint-exit
Utility to handle pylint exit codes in an OS-friendly way.

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

# Example
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

This list is stored in `EXIT_CODES_LIST`, which can be customised if needed.

