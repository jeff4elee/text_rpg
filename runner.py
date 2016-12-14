from dungeon import *
from player import *

t1 = Town(name="T1")
t2 = Town(name="T2")
d1 = Town(name="D1")
g = Graph()
g.add_vertices([t1, t2, d1])
g.add_edges([[t1, t2], [t1, d1], [d1, t1], [t2, d1]])
g.display_graph()
n = NodeTraverser()
#n.enter_map(g, g.get_vertex(t1))


r1 = Room(1)
r2 = Room(2)
r3 = Room(3)
r4 = Room(4)
g2 = Graph()
g2.add_vertices([r1, r2, r3, r4])
g2.add_edges([[r1, r2], [r2, r3], [r3, r4], [r4, r3], [r3, r2], [r2, r1]])
g2.display_graph()
n2 = Player("Bob")
n2.enter_map(g2, g2.get_vertex(r1))
