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

    def describe(self):
        return '[%s] From %s to %s (w: %s)' % (self._name, self._source, self._destination, self._weight)

    def __repr__(self):
        return '%s, %s: %s -> %s' % (self._name, self._weight, self._source, self._destination)


class Graph:
    def __init__(self, vertices, data=None, filepath=None, skip_header=False):
        self.data = []
        if filepath:
            self.get_from_file(filepath, skip_header=skip_header)
        elif data:
            self.data = [Edge(i, weight=data[0], source=data[1], destination=data[2])
                         for i in range(len(data))]
        else:
            raise ValueError('No initialization data provided!')
        self.vertices = [i+1 for i in range(vertices)]

    @property
    def v(self):
        return len(self.vertices)

    def get_from_file(self, filepath, skip_header=False):
        data = open(filepath, 'r').readlines()
        data = [d.strip().split(',') for d in data]
        if skip_header:
            data = data[1:]
        print(data)
        self.data = [Edge(i, weight=int(data[i][0]), source=int(data[i][1]),
                          destination=int(data[i][2])) for i in range(len(data))]

    def kruskal(self):
        self.data.sort(key=lambda x: x.w)


g = Graph(4, filepath='trees/1.txt')
print(g.data)
g.kruskal()
print(g.data)
