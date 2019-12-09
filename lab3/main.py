class Edge:
    def __init__(self, name, weight=-1, source=-1, destination=-1):
        self._name = name
        self._source = source
        self._destination = destination
        self._weight = weight

    @property
    def s(self):
        return self._source

    @property
    def d(self):
        return self._destination

    @property
    def w(self):
        return self._weight

    def __eq__(self, other):
        return self.s == other.s and self.d == self.d and self.w == self.w

    def contains_two_trees(self):
        return not self._source == self._destination

    def describe(self):
        return '[%s] From %s to %s (w: %s)' % (self._name, self._source, self._destination, self._weight)

    def __repr__(self):
        return '%s, %s: %s -> %s' % (self._name, self._weight, self._source, self._destination)


class Graph:
    def __init__(self, vertices=None, data=None, filepath=None, skip_header=False):
        self.data = []
        if filepath:
            self.get_from_file(filepath, skip_header=skip_header)
        elif data:
            self.data = [Edge('I am ' + str(i), weight=data[0], source=data[1], destination=data[2])
                         for i in range(len(data))]
        else:
            raise ValueError('No initialization data provided!')
        if vertices:
            self.vertices = vertices
        else:
            self.vertices = set()
            for edge in self.data:
                self.vertices.add(edge.s)
                self.vertices.add(edge.d)
                self.vertices = list(self.vertices)
        self.parents = {vertex: vertex for vertex in self.vertices}
        self.ranks = {vertex: 0 for vertex in self.vertices}
        self.max_weight = max(self.data, key=lambda x: x.w).w
        self.mst = []

    @property
    def v(self):
        return len(self.vertices)

    def get_from_file(self, filepath, skip_header=False):
        data = open(filepath, 'r').readlines()
        data = [d.strip().split(',') for d in data]
        if skip_header:
            data = data[1:]
        print(data)
        self.data = [Edge('I am ' + str(i), weight=int(data[i][0]), source=int(data[i][1]),
                          destination=int(data[i][2])) for i in range(len(data))]

    def kruskal_find(self, vertex):
        if self.parents[vertex] != vertex:
            self.parents[vertex] = self.kruskal_find(self.parents[vertex])
        return self.parents[vertex]

    def kruskal_union(self, source, destination):
        source_root = self.kruskal_find(source)
        dest_root = self.kruskal_find(destination)
        if source_root != dest_root:
            if self.ranks[source_root] > self.ranks[dest_root]:
                self.parents[dest_root] = source_root
            else:
                self.parents[source_root] = dest_root
            if self.ranks[source_root] == self.ranks[dest_root]:
                self.ranks[dest_root] += 1

    def kruskal(self):
        self.data.sort(key=lambda x: x.w)
        for edge in self.data:
            if self.kruskal_find(edge.s) != self.kruskal_find(edge.d):
                self.kruskal_union(edge.s, edge.d)
                self.mst.append(edge)
        self.mst.sort(key=lambda x: x.w)
        print(self.mst)

    def prim(self):
        costs = [self.max_weight + 1] * len(self.vertices)
        edges = [None] * len(self.vertices)
        result_forest = []
        not_needed = []
        for i in range(len(self.vertices)):
            appearances = [edge for edge in self.data
                           if edge.d == self.vertices[i]]
            best_match = min(appearances, key=lambda x: x.w)
            result_forest.append(best_match)
            if not edges[i]:
                edges[i] =

g = Graph(filepath='trees/2.txt')
# print(g.data)
# g.kruskal()
# print(g.data)
