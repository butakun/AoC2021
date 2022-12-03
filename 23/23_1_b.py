"""
#############
#...........#
###D#D#B#A###
  #B#C#A#C#
  #########

Positions
0 1    2    3    4    5 6
    7     9   11   13
    8    10   12   14
State
Empty = 0
A = 1, B = 2, C = 3, D = 4 
 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
[0 0 0 0 0 0 0 4 2 4  3  2  1  1  3]
"""

ASCII_GRAPH = """
01*2*3*4*56
..7.9.b.d..
..8.a.c.e..
""".strip("\n")

from collections import defaultdict
from dijkstra import dijkstra

def build_graph(ascii_graph):
    lines = ascii_graph.split("\n")
    jdim = len(lines[0])
    idim = len(lines)
    print(f"graph = {idim} x {jdim}")

    def convert(c):
        if c in "0123456789":
            return int(c)
        elif c in "abcdef":
            v = 10 + (ord(c) - ord("a"))
            assert v < 16
            return v
        elif c == "*":
            return -1

    grid = [[None for i in range(jdim)] for i in range(idim)]
    negative = -1
    for i in range(idim):
        for j in range(jdim):
            char = lines[i][j]
            if char == ".":
                continue
            node = convert(char)
            if node < 0:
                node = negative
                negative -= 1
            grid[i][j] = node

    graph = {}
    for i in range(idim):
        for j in range(jdim):
            node = grid[i][j]
            if node is None:
                continue
            # find neighbors
            neighbors = []
            indices = []
            if i > 0:
                indices.append([i-1, j])
            if i < idim - 1:
                indices.append([i+1, j])
            if j > 0:
                indices.append([i, j-1])
            if j < jdim - 1:
                indices.append([i, j+1])
            for ii, jj in indices:
                nei = grid[ii][jj]
                if nei is not None:
                    neighbors.append(nei)
            print(f"{node} -> {neighbors}")
            graph[node] = neighbors

    return graph, grid


def build_paths(graph):
    paths = defaultdict(dict)
    for src in range(15):
        for dest in range(15):
            if src == dest:
                continue
            path, dist = dijkstra(graph, src, dest)
            paths[src][dest] = path
    return paths


def path_passable(current, path):
    for node in path[1:]:
        if node >= 0 and current[node] != 0:
            return False
    return True


def next_states_for(G, paths, current, my_pos):
    me = current[my_pos]
    my_rooms = [6 + 2 * me, 6 + 2 * me - 1]

    next_states = []
    for dest in range(15):
        if current[dest] != 0:
            # destination is occupied
            continue
        if my_pos <= 6:
            # i'm in the hallway
            if dest not in my_rooms: 
                continue
        else:
            # i'm in a side room
            if dest <= 6 or dest in my_rooms:
                pass  # ok
            else:
                # can't move to someone else's room
                continue
        # at least it's a legal move, 
        path = paths[my_pos][dest]
        passable = path_passable(current, path)
        if not passable:
            continue

        # and it's passable
        n_steps = len(path) - 1
        energy_per_step = pow(10, me - 1)
        energy = n_steps * energy_per_step

        next_state = current.copy()
        next_state[my_pos] = 0
        next_state[dest] = me
        next_states.append([next_state, energy])

    return next_states


def next_states_all(G, paths, current):
    next_states = []
    for pos in range(15):
        if current[pos] != 0:
            next_states.extend(next_states_for(G, paths, current, pos))
    return next_states


def state_to_str(state, grid):
    print("".join([str(v) for v in state]))
    idim = len(grid)
    jdim = len(grid[0])
    buf = []
    for i in range(idim):
        bufLine = []
        for j in range(jdim):
            c = "#" if grid[i][j] is None else "."
            bufLine.append(c)
        buf.append(bufLine)

    def find_loc(loc):
        for i in range(idim):
            for j in range(jdim):
                if grid[i][j] == loc:
                    return i, j
        raise ValueError

    for loc, v in enumerate(state):
        i, j = find_loc(loc)
        if v == 1:
            c = 'A'
        elif v == 2:
            c = 'B'
        elif v == 3:
            c = 'C'
        elif v == 4:
            c = 'D'
        else:
            c = "."
        buf[i][j] = c

    flattened = "\n".join(["".join(line) for line in buf])
    return flattened

def ascii_to_state(ascii):
    """
    ...........
    ##D#D#B#A##
    ##B#C#A#C##
    """
    coord_to_index = [
    [  0,  1, -1,  2, -1,  3,  -1,  4, -1,  5,  6 ], 
    [ -1, -1,  7, -1,  9, -1,  11, -1, 13, -1, -1 ], 
    [9 -1, -1,  8, -1, 10, -1,  12, -1, 14, -1, -1 ], 
    ]
    lines = [ line.strip() for line in ascii.split("\n") ]
    idim = len(lines)
    jdim = len(lines[0])
    state_dim = max([ max(l) for l in coord_to_index ]) + 1

    state = [ 0 ] * state_dim
    for i in range(idim):
        for j in range(jdim):
            index = coord_to_index[i][j]
            if index < 0:
                continue
            char = lines[i][j]
            if char not in "ABCD":
                continue
            who = ord(char) - ord('A') + 1
            state[index] = who
    return state


class StateNode(object):
    def __init__(self, state):
        self.state = state

    def __hash__(self):
        return hash("".join([str(v) for v in self.state]))

    def __lt__(self, value):
        return hash(self) < hash(value)

    def __eq__(self, value):
        return self.state == value.state

    def __repr__(self):
        return "".join([str(v) for v in self.state])

class StateGraph(object):
    def __init__(self, graph, paths):
        self._graph = graph  # physical graph of the map
        self._paths = paths

    def __getitem__(self, from_state):
        next_states = next_states_all(self._graph, self._paths, from_state.state)
        next_nodes = [[StateNode(state), weight] for state, weight in next_states]
        return next_nodes


def main():

    print(ASCII_GRAPH)
    G, grid = build_graph(ASCII_GRAPH)
    paths = build_paths(G)

    src = 9
    for dest, path in paths[src].items():
        print(f"{src}->{dest}: {path}")

    initial_ascii = """
    ...........
    ##D#C#D#B##
    ##C#A#A#B##
    """.strip()
    initial_state = ascii_to_state(initial_ascii)
    print(state_to_str(initial_state, grid))

    goal_ascii = """
    ..........A
    ##D#D#B#.##
    ##B#C#A#C##
    """.strip()

    goal_ascii = """
    ...........
    ##A#B#C#D##
    ##A#B#C#D##
    """.strip()
    goal_state = ascii_to_state(goal_ascii)
    print(goal_state)

    SG = StateGraph(G, paths)
    initial_node = StateNode(initial_state)
    goal_node = StateNode(goal_state)
    for nei, weight in SG[initial_node]:
        print(f"weight = {weight}")
        print(state_to_str(nei.state, grid))

    solution, energy = dijkstra(SG, initial_node, goal_node, debug_freq=1000)
    for i, node in enumerate(solution):
        print(f"{i}: {node}")
        print(state_to_str(node.state, grid))
    print(f"found the shortest path to {dest} for energy {energy}")


if __name__ == "__main__":
    main()
