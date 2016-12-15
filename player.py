from graph import Graph
from item import *
import conf

class Unit(object):
    def __init__(self, name=None, dct=None):
        self._name = name
        self._health = dct[conf.HEALTH_DATA] if dct else conf.DEFAULT_HEALTH
        self._max_health = dct[conf.MAX_HEALTH_DATA] if dct else conf.DEFAULT_HEALTH
        self._mana = dct[conf.MANA_DATA] if dct else conf.DEFAULT_MANA
        self._max_mana = dct[conf.MAX_MANA_DATA] if dct else conf.DEFAULT_MANA
        self._power = dct[conf.POWER_DATA] if dct else conf.DEFAULT_POWER
        
    def get_health(self):
        """ Returns the unit's current health """
        return self._health

    def set_health(self, health):
        """ Sets the unit's health (no greater than its max) """
        if(health > self._max_health):
            self._health = self._max_health
        else:
            self._health = health

    def get_max_health(self):
        """ Returns the unit's health cap """
        return self._max_health

    def set_max_health(self, max_health):
        """ Sets the unit's health cap """
        self._max_health = max_health
        
    def get_mana(self):
        """ Returns the unit's current mana """
        return self._mana

    def set_mana(self, mana):
        """ Sets the unit's current mana (no greater than its max) """
        if(mana > self._max_mana):
            self._mana = self._max_mana
        else:
            self._mana = mana

    def get_max_mana(self):
        """ Returns the unit's mana cap """
        return self._max_mana
    
    def set_max_mana(self, max_mana):
        """ Sets the unit's mana cap """
        self._max_mana = max_mana
        
    def get_power(self):
        """ Returns the unit's power """
        return self._power

    def set_power(self, power):
        """ Sets the unit's power """
        self._power = power

    def attack(self, unit):
        """ Reduces another unit's health by this unit's power """
        unit.set_health(unit.get_health() - self._power)

    def encode(self):
        """ Returns the unit's properties and type as a dictionary """
        return {self.__class__.__name__: self.get_dict()}

    def get_dict(self):
        """ Returns the unit's properties as a dictionary """
        return {conf.HEALTH_DATA: self._health,
                conf.MAX_HEALTH_DATA: self._max_health,
                conf.MANA_DATA: self._mana,
                conf.MAX_MANA_DATA: self._max_mana,
                conf.POWER_DATA: self._power}

    @staticmethod
    def from_dict(dct):
        """ Accepts a dictionary of properties to
            set the unit's health, mana, and power """

        return Unit(dct=dct)

    def get_name(self):
        return self._name

    def __str__(self):
        return str(self._name) + ':\n' + \
               "Health: " + str(self.get_health()) + \
               '/' + str(self.get_max_health())

    @staticmethod
    def generate(health, mana, power, name=None):
        return Unit(name,
                    {conf.HEALTH_DATA: health,
                     conf.MAX_HEALTH_DATA: health,
                     conf.MANA_DATA: mana,
                     conf.MAX_MANA_DATA: mana,
                     conf.POWER_DATA: power})
    
class Monster(Unit):
    
    def __init__(self, name=None, dct=None, loot=None):
        super(Monster, self).__init__(name=name, dct=dct)
        self._loot = loot if loot else None

    def get_loot(self):
        return self._loot

    @staticmethod
    def generate(health, mana, power, loot, name=None):
        return Monster(name,
                       {conf.HEALTH_DATA: health,
                        conf.MAX_HEALTH_DATA: health,
                        conf.MANA_DATA: mana,
                        conf.MAX_MANA_DATA: mana,
                        conf.POWER_DATA: power},
                       loot)
    
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

    def __init__(self, name, dct=None, inventory=None, equipped=None,
                 graph=None, home_town=None):
        
        super(Player, self).__init__(name=name, dct=dct,
                                     graph=graph, home_town=home_town)
        
        self._inventory = inventory if inventory else []

        #dict comprehension that uses str representation of bits as keys
        self._equipped = {str(slot.value): None for slot in \
                          Slot.__members__.values()}

        #equip the items within the given equipped argument
        if equipped:
            for item in equipped:
                self._equipped[str(item.get_slot())] = item

    def display_stats(self):
        print self.get_name()
        
        print "Health: " + str(self.get_health()) + "/" + \
              str(self.get_max_health())

        print "Mana: " + str(self.get_mana()) + "/" + \
              str(self.get_max_mana())
        
        print "Power: " + str(self.get_power())

        print "Inventory:",

        self.display_inventory()
        
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
            return True
        else:
            print "Item does not exist"
            return False
                
    def get_equipped(self):
        return self._equipped    

    def display_equipped(self):
        """ Neatly displays the instance's equipment and stats """
        
        #iterates through the equipped dictionary, displaying each
        #items stats in a neat fashion
        for slot, item in self._equipped.iteritems():
    
            if not item:
                
                print Slot(int(slot)).name + ": Empty"

                continue
            
            item_data = item.get_dict()
            stats = ""

            #appends the stats string the bonuses the item provides
            if(conf.POWER_DATA in item_data.keys()):
                stats += " Power: +" + str(item_data[conf.POWER_DATA])
            if(conf.HEALTH_DATA in item_data.keys()):
                stats += " Health: +" + str(item_data[conf.HEALTH_DATA])
            if(conf.MANA_DATA in item_data.keys()):
                stats += " Mana: +" + str(item_data[conf.MANA_DATA])
                
            print Slot(int(slot)).name + ": " + str(item) + \
                  "[" + stats + " ]"
            
        
    def equip(self, item):
        """ Equips an item if it exists in the player's inventory """

        #checks if the item is in the inventory, or if
        #the item will equipped no matter what
        if self.remove_from_inventory(item):
        
            #TODO use bitmaps for a slot system
            for slot in self._equipped.iterkeys():
    
                slot_value = int(slot)

                #check what slots the item uses
                if slot_value & item.get_slot() != 0:
                    self.unequip(slot)

            self._equipped[str(item.get_slot())] = item

            item_data = item.get_dict()

            #applies any bonuses the item has
            if(conf.POWER_DATA in item_data.keys()):
                self._power += item_data[conf.POWER_DATA]
            if(conf.HEALTH_DATA in item_data.keys()):
                self._health += item_data[conf.HEALTH_DATA]
            if(conf.MANA_DATA in item_data.keys()):
                self._mana += item_data[conf.MANA_DATA]

    def unequip(self, slot):

        if self._equipped[slot]:

            item = self._equipped[slot]
            item_data = item.get_dict()

            #remove any bonuses the item has
            if(conf.POWER_DATA in item_data.keys()):
                self._power -= item_data[conf.POWER_DATA]
            if(conf.HEALTH_DATA in item_data.keys()):
                self._health -= item_data[conf.HEALTH_DATA]
            if(conf.MANA_DATA in item_data.keys()):
                self._mana -= item_data[conf.MANA_DATA]

            self._equipped[slot] = None
            self.add_to_inventory(item)

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

        equipped = []
        
        #inserts a list of the player's equipped items into the dictionary
        for item in self._equipped.itervalues():
            if item:
                equipped.append(str(item))
                
        data_dict[conf.EQUIP_DATA] = equipped
        
        return data_dict

    @staticmethod   
    def from_dict(dct):
        """ Accepts a dictionary of properties to
            set the unit's name, health, mana, and power """

        inventory = dct.pop(conf.INVENTORY_DATA)
        equipped = dct.pop(conf.EQUIP_DATA)
        home_town = dct.pop(conf.HOME_TOWN_DATA)
        
        return Player(name=dct['name'], dct=dct, inventory=inventory,
                      equipped=equipped, home_town=home_town)
      
