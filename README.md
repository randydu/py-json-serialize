# py-json-serialize

Serialize in JSON format

Features:

- Simple api: @json_serialize, to_json(), from_json();
- Version support: version-based data migration;

## Install

```sh
pip install py-json-serialize
```

## Test

in the project's root folder, run pytest:

```bash
pytest
```

## Dependencies

None

## API

- class decortator __@json_serialize__

  - format 1: no parameter

   ```python
    from py_json_serialize import json_serialize

    @json_serialize
    class A(object):pass
    ```

  - format 2: with parameter

  @json_serialize(clsid = "", [version=0*|n])

    1. _clsid_: the unique string to identify the class. the class-id will be the name of decorated if 
      not specified.
    2. _version_: optional parameter to specify the version of serialized data format. the default value 
    is *0* if not specified.

   ```python
    from py_json_serialize import json_serialize

    # old version
    @json_serialize("app-config", version=1)
    class AppConfigV1(object):
        servers = []

    # new version
    @json_serialize("app-config", version=2)
    class AppConfigV2(AppConfigV1):
        timeout = 600
    ```

- to_json()/from_json()

    The decorated class will have two new functions:

    1. to_json(): convert class instance to json string

        ```python
        @json_serialize
        class Hello(object):
            def __init__(self, who = "World"):
                self.who = who

        a = Hello()
        print(a.to_json())
        ```

        outputs:

        ```json
        {
            "_clsid_": "Hello",
            "who": "World"
        }
        ```

    2. from_json(): reads json string to return an class object.

        It is actually a *staticmethod* that can be called to return an object of any type deduced from the class-id in the data string.
        so don't be surprised that you might get an object of different type if the input json data string is serialized from another class.

        So the from_json() is simply a handy helper method to make your code more readable if your app only handles one type of data. 
  
- function __json_decode__(jstr: str)-> object: convert json string to python object 

    This is a function to decode the serialized json string, its typical usage is as following:

    ```python
    class Task(object):pass
        @staticmethod
        def from_json(jstr):
            return json_decode(jstr)

    @json_serialize
    class CopyFile(Task):pass

    @json_serialize
    class UploadFile(Task):pass

    task1 = Task.from_json("{ '_clsid_':'CopyFile' }")
    assert isinstance(task1, CopyFile)

    task2 = Task.from_json("{ '_clsid_':'UploadFile' }")
    assert isinstance(task2, UploadFile)
    ```

- function __json_encode__ : convert python object to json string 

    ```python

    def json_encode(obj, pretty = True, encode_all_fields = False)

    ```

    When *pretty* is True, the fields are sorted by their name and the json string
    is intented properly for human reading, otherwise the json string can save some
    storage space and more efficient for machine processing.

    If *encode_all_fields* is true, then all class fields are serialized, otherwise 
    the internal fields (field name starts with '_') are ignored.


## Example



## Limitation

