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
        return 'Edge (W %s, S %s, D %s)' % (self._weight, self._source, self._destination)
        # return '(%s, %s, %s)' % (self._source-1, self._destination-1, self._weight)


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
            self.vertices = set(vertices)
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
        self.data = [Edge('V <{0}>'.format(str(i)), weight=int(data[i][0]), source=int(data[i][1]),
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

    def build_adjacency_matrix(self):
        m = [[0] * len(self.vertices) for _ in range(len(self.vertices))]
        for edge in self.data:
            m[edge.s][edge.d] = edge.w
            m[edge.d][edge.s] = edge.w

        return m

    def boruvka_combine(self, setMatrix, e):
        e0 = -1
        e1 = -1
        for i in range(0, len(setMatrix)):
            if e[0] in setMatrix[i]:
                e0 = i
            if e[1] in setMatrix[i]:
                e1 = i
        setMatrix[e0] += setMatrix[e1]
        del setMatrix[e1]

    def boruvka(self):
        adjacency_matrix = self.build_adjacency_matrix()
        set_matrix = [[i] for i in self.vertices]
        tmp = []
        while len(set_matrix) > 1:
            edges = []
            for component in set_matrix:
                edge = [999, [0, 0]]
                for vertex in component:
                    for i in range(0, len(adjacency_matrix[0])):
                        if i not in component and adjacency_matrix[vertex][i] != 0:
                            if edge[0] > adjacency_matrix[vertex][i]:
                                edge[0] = adjacency_matrix[vertex][i]
                                edge[1] = [vertex, i]
                if edge[1][0] > edge[1][1]:
                    edge[1][0], edge[1][1] = edge[1][1], edge[1][0]
                if edge[1] not in edges:
                    edges.append(edge[1])
            for e in edges:
                self.boruvka_combine(set_matrix, e)

    def boruvka_save(self):
        adjacency_matrix = self.build_adjacency_matrix()
        set_matrix = [[i] for i in self.vertices]
        tmp = []
        while len(set_matrix) > 1:
            edges = []
            for component in set_matrix:
                edge = [999, [0, 0]]
                for vertex in component:
                    for i in range(0, len(adjacency_matrix[0])):
                        if i not in component and adjacency_matrix[vertex][i] != 0:
                            if edge[0] > adjacency_matrix[vertex][i]:
                                edge[0] = adjacency_matrix[vertex][i]
                                edge[1] = [vertex, i]
                if edge[1][0] > edge[1][1]:
                    edge[1][0], edge[1][1] = edge[1][1], edge[1][0]
                if edge[1] not in edges:
                    edges.append(edge[1])
            for e in edges:
                self.boruvka_combine(set_matrix, e)
            tmp = edges
        for edge in tmp:
            vertex = [
                v for v in self.data
                if v.s == edge[0] and v.d == edge[1]
                or v.d == edge[0] and v.s == edge[1]
            ]
            self.mst.append(vertex[0])


if __name__ == '__main__':
    kruskal_g = Graph(filepath='trees/2.txt')
    boruvka_g = Graph(filepath='trees/2.txt')
    from timeit import timeit
    times = 100000
    kruskal_time = timeit(kruskal_g.kruskal, number=times)
    boruvka_time = timeit(boruvka_g.boruvka, number=times)
    boruvka_g.boruvka_save()
    print('Kruskal result: ', kruskal_g.mst)
    print('Kruskal time: ', kruskal_time)
    print('Boruvka result: ', boruvka_g.mst)
    print('Boruvka time: ', boruvka_time)