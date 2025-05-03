# Python 2.7 Compatibility Guide

## Overview

CODESYS uses IronPython 2.7 for its scripting environment. This means all scripts that run directly in CODESYS must be compatible with Python 2.7 syntax and features. This guide outlines key differences and considerations for maintaining compatibility between the Python 2.7 code running in CODESYS and any Python 3.x code running in the REST API server.

## Key Differences

### 1. Print Statement vs. Function

**Python 2.7:**
```python
print "Hello, World!"  # Statement without parentheses
```

**Python 3.x:**
```python
print("Hello, World!")  # Function with parentheses
```

### 2. Exception Handling

**Python 2.7:**
```python
try:
    # Code that might raise an exception
    pass
except Exception, e:
    # Handle exception
    print "Error:", str(e)
```

**Python 3.x:**
```python
try:
    # Code that might raise an exception
    pass
except Exception as e:
    # Handle exception
    print("Error:", str(e))
```

### 3. Division Operator

**Python 2.7:**
```python
result = 5 / 2  # Results in 2 (integer division)
float_result = 5.0 / 2  # Results in 2.5 (float division)
```

**Python 3.x:**
```python
result = 5 / 2  # Results in 2.5 (float division)
int_result = 5 // 2  # Results in 2 (integer division)
```

### 4. String and Unicode Types

**Python 2.7:**
```python
str_value = "Hello"  # str type
unicode_value = u"Hello"  # unicode type
```

**Python 3.x:**
```python
str_value = "Hello"  # All strings are Unicode by default
bytes_value = b"Hello"  # For byte strings
```

### 5. Dict Methods

**Python 2.7:**
```python
d = {"key": "value"}
keys = d.keys()  # Returns a list
items = d.items()  # Returns a list of tuples
```

**Python 3.x:**
```python
d = {"key": "value"}
keys = d.keys()  # Returns a view object
items = d.items()  # Returns a view object
```

### 6. xrange and range

**Python 2.7:**
```python
for i in xrange(1000000):  # More memory efficient
    pass
    
for i in range(10):  # Creates a list in memory
    pass
```

**Python 3.x:**
```python
for i in range(1000000):  # Like xrange in Python 2, memory efficient
    pass
```

### 7. Input Functions

**Python 2.7:**
```python
user_input = raw_input("Enter something: ")  # Always returns a string
evaluated_input = input("Enter an expression: ")  # Evaluates the input as Python code
```

**Python 3.x:**
```python
user_input = input("Enter something: ")  # Always returns a string
```

### 8. HTTPServer Module

**Python 2.7:**
```python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse
```

**Python 3.x:**
```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
```

## Best Practices for Cross-Version Compatibility

### 1. Use `__future__` Imports in Python 2.7 Code

```python
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
```

These imports make Python 2.7 behave more like Python 3.x, but may not be fully supported in all IronPython implementations.

### 2. Explicit String Encoding/Decoding

When dealing with binary data or file I/O:

```python
# Python 2.7
with open(file_path, 'rb') as f:
    binary_data = f.read()
    
text_data = binary_data.decode('utf-8')
```

### 3. Use `io.open` Instead of `open` in Python 2.7

```python
import io

with io.open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()
```

### 4. Class Inheritance

```python
# Python 2.7
class MyClass(object):  # Explicitly inherit from object for new-style classes
    def __init__(self):
        pass
```

### 5. String Formatting

Use format() method instead of % operator:

```python
# Works in both Python 2.7 and 3.x
message = "Hello, {0}".format(name)
```

## CODESYS-Specific Considerations

### 1. IronPython Limitations

IronPython may not support all standard Python 2.7 libraries. Always test scripts directly in CODESYS.

### 2. .NET Integration

IronPython can directly use .NET libraries, which can be an advantage:

```python
import System  # .NET library
from System import DateTime

current_time = DateTime.Now
```

### 3. Script Execution Context

Scripts in CODESYS run in a specific context with available global objects. Always handle cases where expected objects might not be available:

```python
# Check if we have a session object
if 'session' in globals():
    system = session.system
else:
    # Create our own system instance
    system = scriptengine.ScriptSystem()
```

## Testing Strategy

1. All scripts intended to run within CODESYS should be tested directly in the CODESYS environment
2. Maintain separate test suites for Python 2.7 and Python 3.x code
3. Use automated tools to verify Python 2.7 compatibility where possible
4. When sending scripts from the REST API to CODESYS, validate the script syntax before execution

## Conclusion

Maintaining compatibility between Python 2.7 and Python 3.x requires careful attention to the differences between the versions. By following these guidelines, you can ensure that your code will work correctly in both the CODESYS scripting environment and in the REST API server.