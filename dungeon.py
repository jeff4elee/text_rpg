import random
import time
import sqlite3
import simplejson as json
import conf
from player import Unit, Monster
from decoder import decode
from graph import Graph

class Room(object):
    
    def __init__(self, room_id, monster_type, monsters=None, exitable=None):
        ''' Sets the room to a unique id, with a monster_type,
            optional monster list and a boolean exit route '''
        self._room_id = room_id
        self._monster_type = monster_type
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

        monster_names = conf.MONSTER_TYPES[self._monster_type]

        for i in range(num_to_generate):

            item_drop = None

            #connection needed to access item table
            con = sqlite3.connect(conf.DATA_BASE)
            cur = con.cursor()

            #decodes a random item in the item table as a loot drop
            #at a rate proportionate to drop_rate / 1
            if random.random() < drop_rate:

                cur.execute("""SELECT json_value FROM Items WHERE Rarity=?""" \
                            """ORDER BY RANDOM() LIMIT 1""",
                            (random.randint(1, difficulty),))
                            
                item_drop = decode(json.loads(cur.fetchone()[0]))
                            
            #generates monsters with various stats
            #health is 4 - 5 times the difficulty
            #power is 2 - 3 times the difficulty
            unit_health = random.randint(difficulty*4, difficulty*5)
            unit_mana = random.randrange(0, 1)
            unit_power = random.randint(difficulty*2, difficulty*3)

            #the name is randomly generated from a list
            #given by the monster type specified
            name = monster_names[random.randint(0, len(monster_names)-1)]
            
            self._monsters.append(Monster.generate(unit_health,
                                                   unit_mana,
                                                   unit_power,
                                                   item_drop,
                                                   name))

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
    def __init__(self, name, monster_type):
        """ Is a graph and takes a name argument. The dungeon
            connects room nodes and is a part of a larger graph """

        super(Dungeon, self).__init__()
        self._name = name
        self._monster_type = monster_type
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
    
    def generate_dungeon(self, num_rooms, difficulty_min,
                         difficulty_max=None, drop_rate=None, linearity=0):
        """ Generates a number of paths/rooms
            of varying ranges/difficulties (if defined) """

        drop_rate = drop_rate if drop_rate else 0
        difficulty_max = difficulty_max if difficulty_max else difficulty_min
        rooms = []
        
        #generates rooms and their monsters, and then links each room together
        for i in range(num_rooms):

            room_difficulty = random.randint(difficulty_min, difficulty_max)
            
            mob_count = random.randrange(1, 4)

            if(i == num_rooms-1):
                room = Room(i, self._monster_type, exitable=True)
            else:
                room = Room(i, self._monster_type)
                
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

