from dungeon import *
from player import *

def init_world(player):

    world_map = Graph()

    town1 = Town(name="Town 1")
    town2 = Town(name="Town 2")
    town3 = Town(name="Town 3")

    dun1 = Dungeon(name="Mick Dungeon", monster_type='Cave',
                   num_rooms=3, difficulty=1, drop_rate=1.0)
    
    dun2 = Dungeon(name="Rick Dungeon", monster_type='Cave',
                   num_rooms=5, difficulty=1, drop_rate=1.0)
    
    dun3 = Dungeon(name="Sick Dungeon", monster_type='Cave',
                   num_rooms=3, difficulty=2, drop_rate=1.0)
    
    dun4 = Dungeon(name="Lick Dungeon", monster_type='Cave',
                   num_rooms=5, difficulty=2, drop_rate=1.0)
    
    world_map.add_vertices([town1, town2, town3, dun1, dun2, dun3, dun4])
    world_map.add_edges([[town1, town2], [town1, dun1], [town1, dun2],
                         [town2, town1], [town2, dun1], [town2, town3],
                         [town3, dun3], [dun1, town2], [dun1, dun2],
                         [dun2, dun3], [dun2, town1], [dun3, dun4],
                         [dun4, town3]])

    if not player.get_home_town():
        player.set_home_town(str(town1))
        player.enter_map(world_map, world_map.get_vertex(str(town1)))
    else:
        player.enter_map(world_map, world_map.get_vertex(player.get_home_town()))
