from player import generateUnit, Unit
import random

class DungeonTraverser():
    def __init__(self, dungeon):
        self._rooms = dungeon.retrieve_rooms()
        self._position = self._rooms[0]
        
    def check_position(self):
        print self._position
        return self._position
    
    def check_exit(self):
        return self._position.exitable()
    
    def check_surroundings(self):
        return self._position.get_str_nodes()

    def proceed_battle(self):
        return self._position.next_monster()
    
    def prompt_next_room(self, room_to_enter=None):

        self.check_surroundings()

        if room_to_enter is not None:
            enter_room_id = room_to_enter
        else:
            enter_room_id = int(raw_input("Type the id of the room you wish to enter next"))
        
        for node in self._position.get_nodes():
            if enter_room_id == node.get_id():
                self._position = node
                break

        print self._position.get_id()
            

class Dungeon():
    def __init__(self, name, rooms=None):
        self._name = name
        self._rooms = rooms if rooms else []

    def retrieve_rooms(self):
        return self._rooms
    
    def display_rooms(self):
        for room in self._rooms:
            print str(room)
    
    def generate_dungeon(self, numToGenerate, difficultyMin, difficultyMax=None, linearity=0):
        """ Generates a number of paths/rooms
            of varying ranges/difficulties (if defined) """

        if not difficultyMax:
            difficultyMax = difficultyMin + 1

        #generates rooms and their monsters, and then links each room together
        for i in range(numToGenerate):

            roomDifficulty = random.randrange(difficultyMin, difficultyMax)
            mobCount = random.randrange(1, 4)

            if(i == numToGenerate-1):
                room = Room(i, exitable=True)
            else:
                room = Room(i)
                
            room.generate_monsters(mobCount, roomDifficulty)
            self._rooms.append(room)
            #currently linear dungeon
            if(i > 0):
                self._rooms[i].add_node(self._rooms[i-1])
                self._rooms[i-1].add_node(self._rooms[i])


class Node():
    
    def __init__(self, nodes=None):
        self._nodes = nodes if nodes else []

    def add_node(self, node):
        """ Links a node (one-sided) to the instance """
        self._nodes.append(node)

    def get_nodes(self):
        """ Returns the list of nodes """
        return self._nodes

    def get_str_nodes(self):
        """ Returns the list of string
            representations of the nodes """
        str_nodes = []
        for node in self._nodes:
            str_nodes.append(str(node))
        return str_nodes

    def __str__(self):
        return "Node"

class Room(Node):
    
    def __init__(self, room_id, nodes=None, monsters=None, exitable=None):
        self._room_id = room_id 
        self._nodes = nodes if nodes else []
        self._monsters = monsters if monsters else []
        self._exitable = exitable if exitable else False

    def get_id(self):
        return self._room_id
    
    def exitable(self):
        """ Returns whether the room has an exit to the outside """
        return self._exitable
    
    def next_monster(self):
        """ Returns the next monster in the list """
        if(self._monsters):
            return self._monsters.pop()

    def generate_monsters(self, numToGenerate, difficulty):
        """ Generates monsters of varying degrees of difficulty
            and adds them to the list of monsters """
        for i in range(numToGenerate):
            unit_health = random.randrange(difficulty*10, difficulty*13)
            unit_mana = random.randrange(0, 1)
            unit_power = random.randrange(difficulty*4, difficulty*6)
            self._monsters.append(generateUnit(unit_health, unit_mana, unit_power))

    def __str__(self):
        """ String representation of a room instance, displaying
            the count of monsters in the room, and whether the
            room is has an exit to the outside """
        room_id = "ID: " + str(self._room_id)
        monster_count = "Monsters: " + str(len(self._monsters))
        exitable = str(self._exitable)
        return room_id + ", " + monster_count + ", " + exitable
