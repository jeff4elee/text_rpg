from dungeon import *
from player import *

def init_world(player):

    world_map = Graph()

    town1 = Town(name="Town 1")
    town2 = Town(name="Town 2")
    town3 = Town(name="Town 3")
    dun1 = Dungeon(name="Dick Dungeon")
    dun2 = Dungeon(name="Rick Dungeon")
    dun1.generate_dungeon(num_to_generate=3, difficulty_min=1, drop_rate=1.0)
    dun2.generate_dungeon(6, 1, drop_rate=1.0)
    world_map.add_vertices([town1, town2, town3, dun1, dun2])
    world_map.add_edges([[town1, dun2], [town2, dun1], [dun1, town3],
                         [town3, town1], [town2, dun2], [dun2, town2]])

    print player.get_home_town()
    if not player.get_home_town():
        player.set_home_town(str(town1))
        player.enter_map(world_map, world_map.get_vertex(str(town1)))
    else:
        player.enter_map(world_map, world_map.get_vertex(player.get_home_town()))
