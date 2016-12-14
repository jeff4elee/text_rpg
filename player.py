from graph import Graph
from dungeon import Unit
from item import *
import conf

class NodeTraverser(Unit):
    def __init__(self, name=None, dct=None, graph=None, home_town=None):
        ''' Takes in a name, the unit's data, the graph/map it is in,
            and the home_town node'''
        
        super(NodeTraverser, self).__init__(name=name, dct=dct)
        self._graphs = [graph] if graph else []
        self._positions = []
        self._home_town = home_town if home_town else None

    def get_current_map(self):
        """ Returns the last graph in the graphs array """
        return self._graphs[-1]
    
    def get_home_town(self):
        """ Retrieves the current home town """
        return self._home_town
    
    def set_home_town(self, home_town):
        """ Mutator to change the home town """
        self._home_town = home_town
            
    def enter_map(self, graph, position):
        """ Appends the graph onto a stack, and sets
            the position of that graph """
        self._graphs.append(graph)
        self._positions.append(position)

    def exit_map(self):
        """ Pops the last graph/position in the graphs/positions stacks """
        self._graphs.pop()
        self._positions.pop()
        print str(self._positions[-1])

        if(self._positions):
            self._position = self._positions[-1]
        
    def get_position(self):
        """ Returns the current node in the graph this unit is in """
        try:
            return self._positions[-1]
        except:
            return "No positions!"

    def set_position(self, position):
        """ Sets the current node in the graph this unit is in """
        if self._positions:
            self._positions[-1] = position
        else:
            self._positions.append(position)
    
    def encode(self):
        """ Returns the unit's properties as a dictionary """
        return {self.__class__.__name__: self.get_dict()}

    def get_dict(self):
        data_dict = super(NodeTraverser, self).get_dict()
        data_dict[conf.HOME_TOWN_DATA] = self._home_town
        return data_dict

    @staticmethod    
    def from_dict(dct):
        """ Accepts a dictionary of properties to
            set the unit's name, health, mana, and power """
        home_town = dct.pop(conf.HOME_TOWN_DATA)
        return NodeTraverser(dct=dct, home_town=home_town)
             
class Player(NodeTraverser):

    def __init__(self, name, dct = None, inventory = None, graph=None, home_town=None):
        super(Player, self).__init__(name=name, dct=dct, graph=graph, home_town=home_town)
        self._inventory = inventory if inventory else []
        self._equipped = []
        
    def proceed_battle(self):
        """ Returns the next monster """
        return self._position.next_monster()

    def display_inventory(self):
        """ Neatly prints out the player's inventory """
        print map(str, self._inventory)

    def get_from_inventory(self, item_name):
        for item in self._inventory:
            if item_name.lower() == str(item).lower():
                return item
        return None
    
    def get_inventory(self):
        """ Returns the player's inventory """
        return self._inventory

    def add_to_inventory(self, item):
        """ Adds an item to the player's inventory """
        self._inventory.append(item)

    def remove_from_inventory(self, item):
        """ Removes a specific item from the player's inventory """
        if item in self._inventory:
            self._inventory.remove(item)
            print "Item successfully removed"
            return True
        else:
            print "Item does not exist"
            return False
        
    def encode(self):
        """ Returns the unit's properties as a dictionary """
        return {self.__class__.__name__: self.get_dict()}

    def get_dict(self):
        """ Returns the dictionary representation of the player """
        data_dict = super(Player, self).get_dict()

        #converts each item into its string representation
        #makes it easier when accessing rows in item table
        data_dict['name'] = self._name
        data_dict[conf.INVENTORY_DATA] = [str(item) for item in self._inventory]
        data_dict[conf.INVENTORY_DATA] += [str(item) for item in self._equipped]
        return data_dict

    @staticmethod   
    def from_dict(dct):
        """ Accepts a dictionary of properties to
            set the unit's name, health, mana, and power """
        #TODO CALL TO ITEM TABLE AND PULL THE JSON FILES OF EACH MATCHING NAME ROW
        inventory = dct.pop(conf.INVENTORY_DATA)

                
        home_town = dct.pop(conf.HOME_TOWN_DATA)
        return Player(name=dct['name'], dct=dct, inventory=inventory, home_town=home_town)
      
    def equip(self, item):
        """ Equips an item if it exists in the player's inventory """

        #checks if the item is i        
        if self.remove_from_inventory(item):
            self._equipped.append(item)

            item_data = item.get_dict()

            if(conf.POWER_DATA in item_data.keys()):
                self._power += item_data[conf.POWER_DATA]
            if(conf.HEALTH_DATA in item_data.keys()):
                self._health += item_data[conf.HEALTH_DATA]
            if(conf.MANA_DATA in item_data.keys()):
                self._mana += item_data[conf.MANA_DATA]

            #TODO use bitmaps for a slot system
            for i in self._equipped:
                if instanceof(i, item):
                    self.unequip(i)
                    break

    def unequip(self, item):

        if item in self._equipped:

            item_data = item.get_dict()

            if(conf.POWER_DATA in item_data.keys()):
                self._power -= item_data[conf.POWER_DATA]
            if(conf.HEALTH_DATA in item_data.keys()):
                self._health -= item_data[conf.HEALTH_DATA]
            if(conf.MANA_DATA in item_data.keys()):
                self._mana -= item_data[conf.MANA_DATA]

            self._equipped.remove(item)
            self.add_to_inventory(item)

                
    def get_equipped(self):
        return self._equipped
    
