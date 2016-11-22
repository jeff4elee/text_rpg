import game_prompts as game
import dungeon as dgn
import unittest

class TestGameLogin(unittest.TestCase):

    def test_default_room(self):
        room1 = dgn.Room(0)
        room1.generate_monsters(1, 1)
        room2 = dgn.Room(0)
        room3 = dgn.Room(2, exitable=True)
        room4 = dgn.Room(2)

        #check that room2 is not instantiated to be
        #the same as room1
        self.assertFalse(str(room1) == str(room2) or
                         str(room3) == str(room4))

    def test_dungeon_traversal(self):
        d = dgn.Dungeon("Test Dungeon")
        d.generate_dungeon(10, 1)
        dt = dgn.DungeonTraverser(d)

        for i in range(len(dt._rooms)):
            dt.prompt_next_room(i)

        self.assertTrue(dt.check_position())
            

#TODO
#    def test_registration(self):
#        game.prompt_registration()

if __name__ == '__main__':
    unittest.main()
