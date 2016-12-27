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
        self._speed = dct[conf.SPEED_DATA] if dct else conf.DEFAULT_SPEED
        self._cspeed = dct[conf.SPEED_DATA] if dct else conf.DEFAULT_SPEED
            
    def get_health(self):
        """ Returns the unit's current health """
        return self._health

    def set_health(self, health):
        """ Sets the unit's health (no greater than its max) """
        if(health > self._max_health):
            self._health = self._max_health
        elif(health < 0):
            self._health = 0
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

    def get_cspeed(self):
        """ Returns the unit's speed """
        return self._cspeed

    def set_cspeed(self, cspeed):
        self._cspeed = cspeed

    def get_speed(self):
        return self._speed
    
    def set_speed(self, speed):
        """ Sets the unit's speed """
        self._speed = speed
        
    def attack(self, unit):
        """ Reduces another unit's health by this unit's power """
        unit.set_health(unit.get_health() - self._power)
        self._cspeed = self._speed

    def encode(self):
        """ Returns the unit's properties and type as a dictionary """
        return {self.__class__.__name__: self.get_dict()}

    def get_dict(self):
        """ Returns the unit's properties as a dictionary """
        return {conf.HEALTH_DATA: self._health,
                conf.MAX_HEALTH_DATA: self._max_health,
                conf.MANA_DATA: self._mana,
                conf.MAX_MANA_DATA: self._max_mana,
                conf.POWER_DATA: self._power,
                conf.SPEED_DATA: self._speed}

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
               '/' + str(self.get_max_health()) + "\n" + \
               "Attack Time: " + str(self.get_cspeed()) + '/' + \
               str(self.get_speed())

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
        self._loot = loot if loot else []

    def get_loot(self):
        return self._loot

    @staticmethod
    def generate(health, mana, power, speed, loot, name=None):
        return Monster(name,
                       {conf.HEALTH_DATA: health,
                        conf.MAX_HEALTH_DATA: health,
                        conf.MANA_DATA: mana,
                        conf.MAX_MANA_DATA: mana,
                        conf.POWER_DATA: power,
                        conf.SPEED_DATA: speed},
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

    def __init__(self, name, dct=None, money=None,
                 inventory=None, equipped=None,
                 graph=None, home_town=None):
        
        super(Player, self).__init__(name=name, dct=dct,
                                     graph=graph, home_town=home_town)

        self._money = money if money else Coins()
        self._inventory = inventory if inventory else []
        self._inventory_display = {}
        
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

        print "Attack Speed: " + str(self.get_speed())
        
        print "Inventory:",

        self.display_inventory()

    def get_money():
        return self._money
    
    def display_inventory(self):
        """ Neatly prints out the player's inventory """
        for item in self._inventory:
            if str(item) in self._inventory_display.keys():
                self._inventory_display[str(item)] += 1
            else:
                self._inventory_display[str(item)] = 1

        self._inventory_display[str(self._money)] = self._money.get_amount() 
        print self._inventory_display

        self._inventory_display.clear()

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
        if(isinstance(item, Coins)):
            self._money.add(item.get_amount())            
        else:
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
            
            item_data = item.get_bonuses()
            stats = ""

            #appends the stats string the bonuses the item provides
            if(conf.POWER_DATA in item_data.keys()):
                stats += " Power: +" + str(item_data[conf.POWER_DATA])
            if(conf.MAX_HEALTH_DATA in item_data.keys()):
                stats += " Health: +" + str(item_data[conf.MAX_HEALTH_DATA])
            if(conf.MAX_MANA_DATA in item_data.keys()):
                stats += " Mana: +" + str(item_data[conf.MAX_MANA_DATA])
            if(conf.SPEED_DATA in item_data.keys()):
                stats += " Speed: +" + str(item_data[conf.SPEED_DATA])
                
            print Slot(int(slot)).name + ": " + str(item) + \
                  " [" + stats + " ]"
            
        
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

            item_data = item.get_bonuses()

            #applies any bonuses the item has
            if(conf.POWER_DATA in item_data.keys()):
                self._power += item_data[conf.POWER_DATA]
            if(conf.MAX_HEALTH_DATA in item_data.keys()):
                self._max_health += item_data[conf.MAX_HEALTH_DATA]
                self._health += item_data[conf.MAX_HEALTH_DATA]
            if(conf.MAX_MANA_DATA in item_data.keys()):
                self._max_mana += item_data[conf.MAX_MANA_DATA]
                self._mana += item_data[conf.MAX_MANA_DATA]
            if(conf.SPEED_DATA in item_data.keys()):
                self._speed -= item_data[conf.SPEED_DATA]
                if(self._cspeed > self._speed):
                    self._cspeed = self._speed

    def unequip(self, slot):

        if self._equipped[slot]:

            item = self._equipped[slot]
            item_data = item.get_bonuses()

            #remove any bonuses the item has
            if(conf.POWER_DATA in item_data.keys()):
                self._power -= item_data[conf.POWER_DATA]
            if(conf.MAX_HEALTH_DATA in item_data.keys()):
                self._max_health -= item_data[conf.MAX_HEALTH_DATA]
                self._health -= item_data[conf.MAX_HEALTH_DATA]

                if(self._health <= 0):
                    self._health = 1
                    
            if(conf.MAX_MANA_DATA in item_data.keys()):
                self._max_mana -= item_data[conf.MAX_MANA_DATA]
                self._mana -= item_data[conf.MAX_MANA_DATA]
            if(conf.SPEED_DATA in item_data.keys()):
                self._speed += item_data[conf.SPEED_DATA]
                self._cspeed += item_data[conf.SPEED_DATA]
                    
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

        data_dict[conf.COIN_AMOUNT] = self._money.get_amount()
        
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
        money = dct.pop(conf.COIN_AMOUNT)
        return Player(name=dct['name'], dct=dct, inventory=inventory,
                      money=Coins(money), equipped=equipped, home_town=home_town)
      
