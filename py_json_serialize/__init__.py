"""
Simple json serialization utility

    Two helper functons (to_json/from_json) added

        @json_serialize
        class A:
            def __init__(self, name):
                self.name = name

        a0 = A('Jack')
        js = a0.to_json()

        a1 = A.from_json(js)
        assert(isinstance(a1, A))
        assert(a0.name == a1.name)

        ==> class-id = 'A'


        @json_serialize()
        class B: pass

        ==> class-id = 'B'

        @json_serialize("my-clsid")
        class C0: pass

        ==> class-id = 'my-clsid'

        @json_serialize("my-cls-id", version=1)
        class C1: pass

        ==> class-id = 'my-clsid:1'

        When deserializing, json_decode() tries to return python object fully
        matching the class-id, if only the version mismatch, it returns the
        python object with the latest version, if matched class-id is found,
        exception JSON_SERIALIZE_ERRORis raised.
Limit:
------

  the class __init__() must have no mandantary positional parameters

  ex:

    @json_serialize
    class Student:
        def __init__(self, name='', age=18):
            self.name = name
            self.age = age


"""

__version__ = "0.9.0"

import json

# the unique key in serialized json object, its value is the full
# identifier of the serialized class
_CLSID = '_CLSID_'


class JsonSerializeError(Exception):
    ''' Exception of Json Serializer '''


def _get_type_key(typ):
    # get a full class identifier from a class type
    return typ.__name__


def _parse_class_id(clsid):  # -> (base, ver)
    parts = clsid.split(':')
    return (parts[0], parts[1] if len(parts) > 1 else 0)


def _get_class_id(base, ver):
    return base if ver == 0 else base + ':' + str(ver)


class _MyJSONEncoder(json.JSONEncoder):
    # customized encoder to support registered classes
    types = {}
    enable_all_fields = False

    @classmethod
    def register_class(cls, new_type, base, ver):
        ''' register a class as serializable '''
        key = _get_class_id(base, ver)
        if key in cls.types:
            raise JsonSerializeError("class '%s' already registered!" % key)

        cls.types[key] = new_type

    @classmethod
    def resolve_class(cls, clsid):
        ''' resolve class type from its class-id '''
        if clsid in cls.types:  # full match
            return cls.types[clsid]

        # version compatibility support

        base, _ = _parse_class_id(clsid)
        try:
            max_ver = max([j[1] for j in [_parse_class_id(i)
                                          for i in cls.types] if j[0] == base])
            return cls.types[_get_class_id(base, max_ver)]
        except ValueError:
            # no version at all
            raise JsonSerializeError("class-ID '%s' not supported!" % clsid)

    def find_clsid_from_object_type(self, obj_type):
        ''' try finding if obj's type is registered (supports json-serialize)? '''
        for clsid, typ in self.types.items():
            if typ == obj_type:
                return clsid
        raise ValueError('object type not registered')

    def default(self, o):
        try:
            clsid = self.find_clsid_from_object_type(type(o))
        except ValueError:
            return super().default(o)
        else:
            # To minimize serialized data size, only instantiated fields are
            # saved and the fields defined in class are ignored.
            result = dict(o.__dict__) if self.enable_all_fields else {
                k: v for k, v in o.__dict__.items() if not k.startswith('_')}
            result[_CLSID] = clsid
            return result

        return super().default(o)


def json_encode(obj, pretty=True, encode_all_fields=False):
    """ convert python object to json string

    if encode_all_fields is true, then all class fields are serialized, otherwise
    the internal fields (field name starts with '_') are ignored.
    """
    encoder = _MyJSONEncoder(
        sort_keys=True, indent=4, ensure_ascii=False) if pretty else \
            _MyJSONEncoder(ensure_ascii=False)
    encoder.enable_all_fields = encode_all_fields
    return encoder.encode(obj)


def json_decode(jstr):
    """ convert json string to python object """

    def resolve_my_types(dic):
        # resolve dictionary object to registered json-serializable class
        # instance
        if _CLSID not in dic:
            return dic

        clsid = dic[_CLSID]
        typ = _MyJSONEncoder.resolve_class(clsid)

        result = typ()
        fields = dir(result)  # all existent fields

        for i in dic:
            if i != _CLSID:
                val = dic[i]

                # adds version migration query logic later...

                # here we only set the existent fields to avoid data polution.
                if i in fields:
                    result.__setattr__(i, val if not isinstance(
                        val, dict) else resolve_my_types(val))

        return result

    return json.loads(jstr, object_hook=resolve_my_types)


def _patch(cls, clsid, version):

    # make sure cls::__init__() does not have mandatary positional parameters
    # maybe we can inspect the cls::__init__() to avoid creating an instance.
    try:
        _ = cls()
    except:
        raise ValueError(
            "class '%s' object cannot be instaniated with empty parameters" \
                % cls.__name__)

    _MyJSONEncoder.register_class(cls, clsid, version)

    # adds some helper functons
    def to_json(self, pretty=True):
        """ serialize as json string """
        return json_encode(self, pretty)

    @staticmethod
    def from_json(jstr):
        return json_decode(jstr)

    cls.to_json = to_json
    cls.from_json = from_json

    return cls


def _json_serialize_no_param(cls):
    """ class decorator to support json serialization

       Register class as a known type so it can be serialized and deserialzied
       properly
    """
    return _patch(cls, _get_type_key(cls), 0)


def _json_serialize_with_param(clsid, **kwargs):
    def wrap(cls):
        return _patch(cls, clsid if clsid != "" else _get_type_key(cls), \
            kwargs.get('version', 0))

    return wrap


def json_serialize(cls_or_id="", **kwargs):
    ''' decorator to specify a class is serializable '''
    if isinstance(cls_or_id, type):
        return _json_serialize_no_param(cls_or_id)

    if not isinstance(cls_or_id, str):
        raise JsonSerializeError(
            "syntax: json_serialize(id, [version=1]), id must be a string")

    return _json_serialize_with_param(cls_or_id, **kwargs)
