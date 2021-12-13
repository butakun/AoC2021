
import numpy as np


def dfs(graph, paths, path, node):
    #print(f"from {node}, path is now {path}")
    path.append(node)
    #print(f"adding {node} to {path}")
    if node == "end":
        print("path found: ", path)
        paths.append(list(path))
        path.pop()
        return 
    for nei in graph[node]:
        if (nei not in path) or (nei.isupper()):
            dfs(graph, paths, path, nei)
        elif (nei in path) and nei.islower():
            # count the number of nei
            small = {}
            twice = False
            for c in path:
                if not c.islower():
                    continue
                if c not in small:
                    small[c] = 1
                else:
                    small[c] += 1
                    twice = True
            if not twice:
                print(f"none appeared twice {small}, so {nei} is possible")
                dfs(graph, paths, path, nei)

    path.pop()

def main(filename):
    def add_edge(graph, v1, v2):
        if v1 not in graph:
            graph[v1] = set([v2])
        else:
            graph[v1].add(v2)

    with open(filename) as f:
        graph = {}
        for line in f:
            fra, til = line.strip().split("-")
            if fra != "end" and til != "start":
                add_edge(graph, fra, til)
            if til != "end" and fra != "start":
                add_edge(graph, til, fra)

    print(graph)
    paths = []
    path = []
    dfs(graph, paths, path, "start")

    print(f"{len(paths)} paths found")

if __name__ == "__main__":
    main("input.txt")
