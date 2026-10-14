import io
from configurables.parse import Configurables_stream_parser, parse_loaders
from configurables import Configurable_class_target, Options, Option


data = """

link:
    tag: Base
    type: partial
    next:
     - fry
     - bake

meta:
    class_name: Cooking

---

link:
    type: partial
    tag: fry
    next:
     - "180"
     - "200"

method: fry

    
---

link:
    type: partial
    tag: bake
    next:
     - "180"
     - "200"

method: bake

---

link:
    tag: "180"

temperature: 180

    
---

link:
    tag: "200"

temperature: 200

"""


class Cooking_parent(Configurable_class_target):

    CLASS_HANDLE = ["Cooking_parent"]


class Cooking(Cooking_parent):

    CLASS_HANDLE = ["Cooking"]
    
    method = Option(choices=['fry','bake'], required = True)
    temperature = Option(type=float, default = 200.0)



def test_parse():
    """"""
    parser = Configurables_stream_parser('cooking_parent')
    parser.parse_stream(io.StringIO(data), 'data')

    assert len(parser.loaders) == 5

def test_load():
    """"""
    # TODO: improve this interface.
    top = parse_loaders({'Cooking_parent': io.StringIO(data)})['Cooking_parent']

    assert len(top) == 4
    assert isinstance(top[0], Cooking)
    assert top[1].method == 'fry'
    assert top[1].temperature == 180
    assert top[2].method == 'fry'
    assert top[2].temperature == 200
    assert top[3].method == 'bake'
    assert top[3].temperature == 180
    assert top[4].method == 'bake'
    assert top[4].temperature == 200
    assert len(list(reversed(top))) == 4
