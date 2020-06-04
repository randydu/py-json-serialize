import pytest
from py_json_serialize import *

def test_class_init():

    with pytest.raises(ValueError):
        @json_serialize
        class A(object):
            def __init__(self, name):
                self.name = name


def test_json_serialize():
    @json_serialize
    class A(object):
        def __init__(self, name=""):
            self.name = name

    a0 = A('Jack')
    js = a0.to_json()
    print(js)

    a1 = A.from_json(js)
    assert(isinstance(a1, A))
    assert(a0.name == a1.name)

def test_inherit():
    @json_serialize
    class People(object):
        sex = ''
        def __init__(self, name=""):
            self.name = name

    @json_serialize
    class Man(People):
        sex = 'male'

    @json_serialize
    class Woman(People):
        sex = 'female'

    @json_serialize
    class Family(object):
        father = None
        mother = None
        son = None

    family = Family()
    family.father = Man('Jason')
    family.mother = Woman('Maria')
    family.son = Man('Tom')

    js = family.to_json()
    print(js)

    f = Family.from_json(js)
    assert isinstance(f, Family)
    assert isinstance(f.father, Man)
    assert isinstance(f.mother, Woman)
    assert isinstance(f.son, Man)

    assert f.father.name == 'Jason'
    assert f.mother.name == 'Maria'
    assert f.son.name == 'Tom'


def test_class_id():
    @json_serialize
    class Hello: 
        who = 'World'

    hello = Hello.from_json({
        CLASS_ID: "Hello",
        "who": "Tom"
    })
    assert isinstance(hello, Hello)
    assert hello.who == 'Tom'