
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

    path.pop()

def main(filename):
    with open(filename) as f:
        graph = {}
        for line in f:
            fra, til = line.strip().split("-")
            if fra not in graph:
                graph[fra] = [til]
            else:
                graph[fra].append(til)
            if fra != "start" and til != "end":
                if til not in graph:
                    graph[til] = [fra]
                else:
                    if fra not in graph[til]:
                        graph[til].append(fra)

    print(graph)
    paths = []
    path = []
    dfs(graph, paths, path, "start")

    print(f"{len(paths)} paths found")

if __name__ == "__main__":
    main("input.txt")
