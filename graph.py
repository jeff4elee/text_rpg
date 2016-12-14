class Graph(object):
    def __init__(self):
        self._vertices = {}
        self._edges = {}

    def add_vertices(self, nodes):
        for node in nodes:
            self.add_vertex(node)
        
    def add_vertex(self, node):
        """ Adds a vertex to the list of vertices
            in the graph """
        self._vertices[str(node)] = node

    def get_vertices(self):
        return self._vertices

    def get_vertex(self, node_key):
        return self._vertices[str(node_key)]

    def add_edges(self, node_pairs):
        for node1, node2 in node_pairs:
            self.add_edge(node1, node2)
            
    def add_edge(self, vertex_one, vertex_two):
        """ Creates a directed edge from vertex_one
            to vertex_two """
        if str(vertex_one) in self._edges:
            self._edges[str(vertex_one)].append(vertex_two)
        else:
            if str(vertex_one) not in self._vertices:
                self.add_vertex(vertex_one)
            self._edges[str(vertex_one)] = [vertex_two]

    def get_edges(self):
        return self._edges

    def get_adjacent_vertices(self, vertex):
        return self._edges[str(vertex)]

    def display_adjacent(self, vertex):
        neighbors = []
        for node in self._edges[str(vertex)]:
            neighbors.append(str(node))
        return neighbors
     
    def display_graph(self):
        """ Prints the graph in readable form """
        vertices = []
        edges = {}

        for vertex in self._vertices.iterkeys():
            vertices.append(vertex)
        print vertices
         
        for vertex in self._edges.iterkeys():
            neighbors = []
            for neighbor in self._edges[vertex]:
                neighbors.append(str(neighbor))
            edges[vertex] = neighbors
        print edges
  
