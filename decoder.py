from player import *
from item import *
from dungeon import *

TYPES = { 'Unit' : Unit,
          'NodeTraverser': NodeTraverser,
          'Player': Player,
          'Item': Item,
          'Potion': Potion,
          'Equippable': Equippable,
          'Coins': Coins,
          'Dungeon': Dungeon}

def decode(dct):
    if len(dct) == 1:
        type_name, value = dct.items()[0]
        type_name = type_name.strip('_')
        if type_name in TYPES:
            return TYPES[type_name].from_dict(value)
    return dct
