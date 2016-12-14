from enum import Enum
from player import *

class FightOptions(Enum):
    Attack = 1
    Use_Item = 2 
    Quit = 3

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
    Display_Stats = 2
    Exit_Town = 3

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
