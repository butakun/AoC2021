import math
import heapq
from collections import defaultdict
import itertools

class PriorityQueue(object):
    
    def __init__(self):
        self._pq = []
        self._tasks = {}
        self._counter = itertools.count()
        self._removed_marker = "REMOVED"

    def push(self, task, priority):
        if task in self._tasks:
            self.remove_task(task)
        count = next(self._counter)
        entry = [priority, count, task]
        self._tasks[task] = entry
        heapq.heappush(self._pq, entry)

    def remove_task(self, task):
        entry = self._tasks.pop(task)
        entry[-1] = self._removed_marker

    def pop(self):
        while self._pq:
            priority, count, task = heapq.heappop(self._pq)
            if task is not self._removed_marker:
                del self._tasks[task]
                return task
        raise KeyError("priority queue is empty")

    def __len__(self):
        return len(self._pq)


def dijkstra(G, src, dest, debug_freq=-1):

    D = defaultdict(lambda:math.inf)
    D[src] = 0
    came_from = {src: None}

    pq = PriorityQueue()
    pq.push(src, priority=D[src])

    iter = 0
    while pq:
        u = pq.pop()
        iter += 1
        assert u is not None

        if debug_freq > 0:
            if iter % debug_freq == 0:
                print(f"iter {iter}: D[u] = {D[u]}")

        if u == dest:
            break
        for v in G[u]:
            try:
                v, weight = v[0], v[1]
            except:
                weight = 1
            dist_v = D[u] + weight
            if dist_v < D[v]:
                D[v] = dist_v
                came_from[v] = u
                pq.push(v, priority=dist_v)

    path = [dest]
    while True:
        prev = came_from[path[-1]]
        if prev is None:
            break
        path.append(prev)

    path.reverse()
    return path, D[dest]


def a_star(G, src, dest):
    pq = PriorityQueue()


def test():
    pq = PriorityQueue()

    pq.push("a", priority=10)
    pq.push("b", priority=1)
    pq.push("c", priority=100)
    while pq:
        print(pq.pop())

    pq.push("A", priority=10)
    pq.push("B", priority=1)
    pq.push("A", priority=0)
    pq.push("C", priority=100)
    while pq:
        print(pq.pop())


if __name__ == "__main__":
    test()
