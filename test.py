import game_prompts as game
from dungeon import *
from player import *
import unittest

class TestGameLogin(unittest.TestCase):

    def test_default_room(self):
        room1 = Room(0)
        room1.generate_monsters(1, 1)
        room2 = Room(0)
        room3 = Room(2, exitable=True)
        room4 = Room(2)

        #check that room2 is not instantiated to be
        #the same as room1
        self.assertFalse(str(room1) == str(room2) or
                         str(room3) == str(room4))

    def test_graph_referencing(self):
        t1 = Town(name="T1")
        t2 = Town(name="T2")
        t3 = Town(name="T3")
        d1 = Dungeon(name="D1")
        d2 = Dungeon(name="D2")
        g = Graph()
        g.add_vertices([t1, t2, t3, d1, d2])
        g.add_edges([[t1, t2], [t1, t3], [t1, d1], [t2, d2]])
        g.add_edge(t2, t3)
        same_reference = g._vertices['T2'] == g._edges['T1'][0]
        same_reference2 = g._vertices['T3'] == g._edges['T1'][1]
        same_reference3 = g._vertices['D2'] == g._edges['T2'][0]
        
        g.display_graph()
        self.assertTrue(same_reference and same_reference2 and same_reference3)
        

#TODO
#    def test_registration(self):
#        game.prompt_registration()

if __name__ == '__main__':
    unittest.main()
