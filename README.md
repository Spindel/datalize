# Datalize:  a simple python3 dataclass serializer and deserializer


This implements a simple `dataclasses.dataclass` serializer and deserializer
for some core Python3 objects that I need. 

So, you have a declared dataclass, and want to transform json loaded objects to
it:
 
    @dataclass
    class Ex:
      val: str
      id: uuid.UUID

    my_json_decoded_data = {'val':'hi', 'id':'029affa6-814e-439a-a61d-2614ad184e0d'}
    obj = datalize.deserialize(json=my_json_decoded_data, target_type=Ex)

Or you have a Dataclass and want to turn it to json:

    @dataclass
    class Example2:
      val: str
      ts: datetime

    # Create an instance of the dataclass
    obj = Example2(name="hello", ts=datetime.now())
    # Serialize turns it into "json-friendly" data format
    prep = datalize.serialize(obj)
    
    # json.dumps turns it into an actual string
    mystr  = json.dumps(prep)
    loaded = json.loads(mystr)
    # Loaded from json again

    # Now we can turn the mangled data back into the python classes, provided
    #that we know the dataclas type.
    obj2 = datalize.deserialize(loaded, target_type=Example2)
    assert obj == obj2


Currently serializes and deserializes:

- Dataclases
- Lists
- Enum
- Datetime  (with and without tz)
- UUID and other "simple" types that can be instantiated from a string ( and cast to string)


## Some choices have been made:

### Enum

Enum are pass-by-value by default, but will _attempt_ to de-serialize using
pass-by-name if it fails to pass-by-value.

Because that behaviour turned out to be what we needed in real life.

### Datetime

Datetimes are serialized to string isoformat and back again.

### UUID

UUID are serialized to a hex-string and back again

### Union

Union defaults to the native encoded type if possible, so the following will
NOT round trip as expected:

    class MyEnum(enum.Enum):
       first = 0

    @dataclass
    class EncodeError:
       num: Union[MyEnum, int]

As it will encode to {"num": 0}  And then back to the int(0).

This should still compare as an int by-value, but may not be what expected.


### Optional

this:

    @dataclass
    class WithOption:
       name: Optional[str]

    deserialize(json={}, target_type=WithOption)

will raise an Exception, as there is no default value for "name".
