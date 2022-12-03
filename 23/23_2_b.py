"""
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

Positions
0 1    2    3    4    5 6
    7    11   15   19
    8    12   16   20
    9    13   17   21 
   10    14   18   22
   
State
Empty = 0
A = 1, B = 2, C = 3, D = 4 
 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
[0 0 0 0 0 0 0 2 4 4  1  3  3  2  4  2  2  1  3  4  1  3  1]
"""

ASCII_GRAPH = [
        "01A2B3C4D56",
        "..7.b.f.j..",
        "..8.c.g.k..",
        "..9.d.h.l..",
        "..a.e.i.m..",
        ]

from collections import defaultdict
from dijkstra import dijkstra, a_star

def build_graph(ascii_graph):
    lines = ascii_graph
    jdim = len(lines[0])
    idim = len(lines)
    print(f"graph = {idim} x {jdim}")

    def convert(c):
        if c in "0123456789":
            return int(c)
        elif c in "abcdefghijklm":
            v = 10 + (ord(c) - ord("a"))
            assert v <= 22
            return v
        elif c in "ABCD":
            v = -(ord(c) - ord("A") + 1)
            return v

    grid = [[None for i in range(jdim)] for i in range(idim)]
    for i in range(idim):
        for j in range(jdim):
            char = lines[i][j]
            if char == ".":
                continue
            node = convert(char)
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
    node_ids = [k for k in graph.keys()]
    paths = defaultdict(dict)
    for src in node_ids:
        for dest in node_ids:
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
    my_rooms = [6 + 4 * me, 6 + 4 * me - 1, 6 + 4 * me - 2, 6 + 4 * me - 3]

    next_states = []
    for dest in range(23):
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
        if dest in my_rooms:
            someone_else_in_my_room = False
            for i in my_rooms:
                if current[i] != 0 and current[i] != me:
                    someone_else_in_my_room = True
                    break
            if someone_else_in_my_room:
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
    for pos in range(23):
        if current[pos] != 0:
            next_states.extend(next_states_for(G, paths, current, pos))
    return next_states


def distance_heuristic(src, dest, paths):
    h = 0
    for me in [4, 3, 2, 1]:
        energy_per_step = pow(10, me - 1)
        i0 = 0
        j0 = 0
        for i in range(4):
            i1 = src[i0:].index(me) + i0
            i0 = i1 + 1
            j1 = dest[j0:].index(me) + j0
            j0 = j1 + 1
            if i1 == j1:
                steps = 0
            else:
                steps = len(paths[i1][j1]) - 1
            h += energy_per_step * steps
    return h


def energy_delta(state1, state2, paths):
    for i1, c1 in enumerate(state1):
        if c1 == 0:
            continue
        if state2[i1] != 0:
            continue
        src = i1
        me = c1
        break
    for i2, c2 in enumerate(state2):
        if c2 == 0:
            continue
        if state1[i2] != 0:
            continue
        dst = i2
        break
    energy_per_step = pow(10, me - 1)
    steps = len(paths[src][dst]) - 1
    return energy_per_step * steps


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

def ascii_to_state(ascii, grid):
    """
    ascii =
    ...........
    ##b#c#b#d##
    ##d#c#b#a##
    ##d#b#a#c##
    ##a#d#c#a##
    """
    lines = [ line.strip() for line in ascii.split("\n") ]
    idim = len(lines)
    jdim = len(lines[0])
    assert idim == len(grid) and jdim == len(grid[0])
    state_dim = max([ max([v for v in l if v is not None]) for l in grid ]) + 1

    state = [ 0 ] * state_dim
    for i in range(idim):
        for j in range(jdim):
            index = grid[i][j]
            if index is None or index < 0:
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


class HFunc(object):
    def __init__(self, goal_node, paths):
        self._goal_state = goal_node.state
        self._paths = paths

    def __call__(self, node):
        return distance_heuristic(node.state, self._goal_state, self._paths)


def main():

    print(ASCII_GRAPH)
    G, grid = build_graph(ASCII_GRAPH)
    paths = build_paths(G)

    src = 10 
    for dest, path in paths[src].items():
        print(f"{src}->{dest}: {path}")

    initial_ascii = """
    ...........
    ##B#C#B#D##
    ##D#C#B#A##
    ##D#B#A#C##
    ##A#D#C#A##
    """.strip()

    initial_ascii = """
    ...........
    ##D#C#D#B##
    ##D#C#B#A##
    ##D#B#A#C##
    ##C#A#A#B##
    """.strip()

    initial_state = ascii_to_state(initial_ascii, grid)
    print(state_to_str(initial_state, grid))

    goal_ascii = """
    B..........
    ##.#C#B#D##
    ##D#C#B#A##
    ##D#B#A#C##
    ##A#D#C#A##
    """.strip()

    goal_ascii = """
    ...........
    ##A#B#C#D##
    ##A#B#C#D##
    ##A#B#C#D##
    ##A#B#C#D##
    """.strip()

    goal_state = ascii_to_state(goal_ascii, grid)
    print(goal_state)
    print(state_to_str(goal_state, grid))

    if False:
        initial_state = [int(c) for c in "12002320003332100114444"]
        print("FROM")
        print(state_to_str(initial_state, grid))

    SG = StateGraph(G, paths)
    initial_node = StateNode(initial_state)
    goal_node = StateNode(goal_state)
    for nei, weight in SG[initial_node]:
        print(f"weight = {weight}")
        print(state_to_str(nei.state, grid))

    H = HFunc(goal_node, paths)
    print("heuristics to goal = ", H(initial_node))

    method = "astar"
    if method == "dijkstra":
        solution, energy = dijkstra(SG, initial_node, goal_node, debug_freq=1000)
    elif method == "astar":
        solution, energy = a_star(SG, initial_node, goal_node, H, debug_freq=1000)

    energy = 0
    for i, node in enumerate(solution):
        print(f"{i}: {node}")
        print(state_to_str(node.state, grid))
        if i > 0:
            state1 = solution[i - 1]
            state2 = node
            delta = energy_delta(state1.state, state2.state, paths)
            energy += delta
            print(f"Energy delta {delta}, total {energy}")

    print(f"found the shortest path to {dest} for energy {energy}")


if __name__ == "__main__":
    main()
