import random
import time
import sqlite3
import simplejson as json
from decoder import decode
from graph import Graph
from conf import DEFAULT_HEALTH, DEFAULT_MANA, DEFAULT_POWER
import conf

class Room(object):
    
    def __init__(self, room_id, monsters=None, exitable=None):
        ''' Sets the room to a unique id, with optional monsters '''
        ''' and exit route '''
        self._room_id = room_id 
        self._monsters = monsters if monsters else []
        self._exitable = exitable if exitable else False

    def get_id(self):
        """ Returns the id of the room """
        return self._room_id
    
    def exitable(self):
        """ Returns whether the room has an exit to the outside """
        return self._exitable
    
    def next_monster(self):
        """ Returns the next monster in the list """
        if(self._monsters):
            return self._monsters.pop()
        return None

    def has_monsters(self):
        """ Returns whether any monsters exist """
        if(self._monsters):
            return True
        return False

    def generate_monsters(self, num_to_generate, difficulty, drop_rate):
        """ Generates monsters of varying degrees of difficulty
            and adds them to the list of monsters """
        for i in range(num_to_generate):

            item_drop = None

            con = sqlite3.connect(conf.DATA_BASE)
            cur = con.cursor()
            
            if random.random() < drop_rate:

                cur.execute("""SELECT json_value FROM Items WHERE Rarity=?""" \
                            """ORDER BY RANDOM() LIMIT 1""",
                            (random.randrange(1, difficulty)))
                            
                item_drop = decode(json.loads(cur.fetchone()[0]))
                            
            #generates monsters with various stats
            #health is 4 - 5 times the difficulty
            #power is 1 - 2 times the difficulty
            unit_health = random.randrange(difficulty*3, difficulty*4)
            unit_mana = random.randrange(0, 1)
            unit_power = random.randrange(difficulty*1, difficulty*2)
            
            self._monsters.append(Monster.generate(unit_health,
                                                   unit_mana,
                                                   unit_power,
                                                   item_drop))

    def __str__(self):
        """ String representation of a room instance, displaying
            the count of monsters in the room, and whether the
            room is has an exit to the outside """

        #TODO
        room_id = "ID: " + str(self._room_id)
        monster_count = "Monsters: " + str(len(self._monsters))
        exitable = str(self._exitable)
        return "Room #" + str(self._room_id)

class Dungeon(Graph):
    def __init__(self, name):
        """ Is a graph and takes a name argument. The dungeon
            connects room nodes and is a part of a larger graph """

        super(Dungeon, self).__init__()
        self._name = name
        self._start = None

    def set_start(self, room):
        self._start = room

    def get_start(self):
        """ Returns the starting room of the dungeon. If the starting
            room is undefined, it returns a random room. If the dungeon
            is empty, it returns an error """

        if not self._start:
            try:
                return random.choice(self._vertices.keys())
            except:
                print "Error, empty dungeon"
        return self._start
    
    def display_rooms(self):
        """ Prints the string representation of all the rooms
            in the dungeon """
        for room in self.get_vertices():
            print str(room)
    
    def generate_dungeon(self, num_to_generate, difficulty_min,
                         difficulty_max=None, drop_rate=None, linearity=0):
        """ Generates a number of paths/rooms
            of varying ranges/difficulties (if defined) """

        drop_rate = drop_rate if drop_rate else 0
        
        if not difficulty_max:
            difficulty_max = difficulty_min

        rooms = []
        
        #generates rooms and their monsters, and then links each room together
        for i in range(num_to_generate):

            room_difficulty = random.randrange(difficulty_min, difficulty_max)
            mob_count = random.randrange(1, 4)

            if(i == num_to_generate-1):
                room = Room(i, exitable=True)
            else:
                room = Room(i)
                
            room.generate_monsters(mob_count, room_difficulty, drop_rate)
            self.add_vertex(room)
            rooms.append(room)
            
            #currently linear dungeon
            if(i > 0):
                self.add_edge(rooms[i-1], rooms[i])
                self.add_edge(rooms[i], rooms[i-1])

    def __str__(self):
        return self._name

                          
class Town():
    def __init__(self, name):
        self._name = name if name else ""

    def __str__(self):
        return self._name

    #TODO town properties


class Unit(object):
    def __init__(self, name=None, dct=None):
        self._name = name
        self._health = dct[conf.HEALTH_DATA] if dct else DEFAULT_HEALTH
        self._max_health = dct[conf.MAX_HEALTH_DATA] if dct else DEFAULT_HEALTH
        self._mana = dct[conf.MANA_DATA] if dct else DEFAULT_MANA
        self._max_mana = dct[conf.MAX_MANA_DATA] if dct else DEFAULT_MANA
        self._power = dct[conf.POWER_DATA] if dct else DEFAULT_POWER
        
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
        return str(self._name) + ': ' + str(self.get_health()) + '/' + str(self.get_max_health())

    @staticmethod
    def generate_unit(health, mana, power, name=None):
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
    def generate_unit(health, mana, power, loot, name=None):
        return Monster(name,
                       {conf.HEALTH_DATA: health,
                        conf.MAX_HEALTH_DATA: health,
                        conf.MANA_DATA: mana,
                        conf.MAX_MANA_DATA: mana,
                        conf.POWER_DATA: power},
                       loot)
