# src: https://stackoverflow.com/a/37237712

def get_parent(pos):
    return (pos + 1) // 2 - 1


def get_children(pos):
    right = (pos + 1) * 2
    left = right - 1
    return left, right


def swap(array, a, b):
    array[a], array[b] = array[b], array[a]


class Heap:

    def __init__(self):
        self._array = []

    def peek(self):
        return self._array[0] if self._array else None

    def _get_smallest_child(self, parent):
        return min([
            it
            for it in get_children(parent)
            if it < len(self._array)
        ], key=lambda it: self._array[it], default=-1)

    def _sift_down(self):
        parent = 0
        smallest = self._get_smallest_child(parent)
        while smallest != -1 and self._array[smallest] < self._array[parent]:
            swap(self._array, smallest, parent)
            parent, smallest = smallest, self._get_smallest_child(smallest)

    def pop(self):
        if not self._array:
            return None
        swap(self._array, 0, len(self._array) - 1)
        node = self._array.pop()
        self._sift_down()
        return node

    def _sift_up(self):
        index = len(self._array) - 1
        parent = get_parent(index)
        while parent != -1 and self._array[index] < self._array[parent]:
            swap(self._array, index, parent)
            index, parent = parent, get_parent(parent)

    def add(self, item):
        self._array.append(item)
        self._sift_up()

    def __bool__(self):
        return bool(self._array)


def backtrack(best_parents, start, end):
    if end not in best_parents:
        return None
    cursor = end
    path = [cursor]
    while cursor in best_parents:
        cursor = best_parents[cursor]
        path.append(cursor)
        if cursor == start:
            return list(reversed(path))
    return None


def dijkstra(weighted_graph, start, end):  # ... , station_popularity)
    """
    Calculate the shortest path for a directed weighted graph.

    Node can be virtually any hashable datatype.

    :param start: starting node
    :param end: ending node
    :param weighted_graph: {"node1": {"node2": weight, ...}, ...}
    :return: ["START", ... nodes between ..., "END"] or None, if there is no
            path
    """
    # TODO: implement skipping empty stations
    distances = {i: float("inf") for i in weighted_graph}
    best_parents = {i: None for i in weighted_graph}

    to_visit = Heap()
    to_visit.add((0, start))
    distances[start] = 0

    visited = set()

    while to_visit:
        src_distance, source = to_visit.pop()
        if src_distance > distances[source]:
            continue
        if source == end:
            break
        visited.add(source)
        for target, distance in weighted_graph[source].items():
            if target in visited:
                continue
            new_dist = distances[source] + weighted_graph[source][target]
            if distances[target] > new_dist:
                distances[target] = new_dist
                best_parents[target] = source
                to_visit.add((new_dist, target))

    return backtrack(best_parents, start, end)

def create_graph(stations, durations):
    graph = {}
    for i, st in enumerate(stations):
        id = st['station_id']
        graph[id] = {}
        for n, st2 in enumerate(stations):
            id2 = st2['station_id']
            if durations[i][n] < 1100:
                graph[id][id2] = durations[i][n]
    return graph

if __name__ == '__main__':
    import json
    METRO = False
    # For metro to work we need to edit original graph - add transit times from bikes to platforms. Just combining it together wont work as there will be key conflict

    with open('data/stations.json', 'r') as f:
        stations = json.load(f)

    with open('data/resp.json', 'r') as f:
        durations = json.load(f)['durations']

    # graph = {"node1": {"node2": weight, ...}, ...}
    graph = create_graph(stations, durations)

    with open('data/graph.json', 'w') as f:
        json.dump(graph, f)

    with open('data/station_names.json', 'r') as f:
        names = json.load(f)

    if METRO:
        with open('data/metro.json', 'r', encoding='UTF-8') as f:
            metro = json.load(f)

        graph = {**metro, **graph}

    # route = dijkstra(graph, '2585349', '2585299')
    # route = dijkstra(graph, '2585299', '2681629')
    # route = dijkstra(graph, '24229285', '2585464')
    # route = dijkstra(graph, "2585913", "2585850")
    
    route = dijkstra(graph, "2681629", "3616030")

    print(route)
    total_time = 0
    for i, id in enumerate(route, 1):
        try:
            print(f"{i}. {names[id]['name']}")
        except KeyError:
            print(f"{i}. {id}")

        try:
            time = graph[id][route[i]]
            total_time += time
            print(f"| {time/60} mins")
        except IndexError:
            pass
    # print(graph['2585349']['2585299'])
    print(f"Total time on this journey: {total_time/60} minutes")