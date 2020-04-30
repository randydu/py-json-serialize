import pytest
from py_json_serialize import json_serialize

def test_err():
    @json_serialize
    class A:
        def __init__(self, name):
            self.name = name

    a = A('Jack')
    with pytest.raises(ValueError):
        a.to_json()


def test_json_serialize():
    @json_serialize
    class A:
        def __init__(self, name=""):
            self.name = name

    a0 = A('Jack')
    js = a0.to_json()
    print(js)

    a1 = A.from_json(js)
    assert(isinstance(a1, A))
    assert(a0.name == a1.name)
