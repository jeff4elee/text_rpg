from enum import Enum
from player import *

class FightOptions(Enum):
    Attack = 1
    Use_Item = 2
    Stats = 3
    Quit = 4

    @classmethod    
    def display(self):
        for o in self:

            to_display = "[" + str(o.value) + ". " + str(o.name) + "]"
            if "_" in o.name:
                to_display = to_display.replace("_", " ")

            print to_display,
        print
        
class TownOptions(Enum):

    Save = 1
    Stats = 2
    Equipment = 3
    Use_Equip = 4
    Exit_Town = 5

    @classmethod
    def display(self):
        for o in self:

            to_display = "[" + str(o.value) + ". " + str(o.name) + "]"

            if "_" in o.name:
                to_display = to_display.replace("_", " ")

            print to_display,
        print
        
class ItemOptions(Enum):

    Use_Equip = 1
    Description = 2
    Cancel = 3

    @classmethod
    def display(self):

        for o in self:
            to_display = "[" + str(o.value) + ". " + str(o.name) + "]"
            if "_" in o.name:
                to_display = to_display.replace("_", "/")

            print to_display,
        print
