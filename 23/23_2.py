import numpy as np
import heapq

"""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

Positions
0 1    2    3    4    5 6
    7     9   11   13
    8    10   12   14
State
Empty = 0
A1 = 1, A2 = 2, B1 = 3, B2 = 4, C1 = 5, C2 = 6, D1 = 7, D2 = 8
 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
[0 0 0 0 0 0 0 3 1 5  7  4  6  8  2]
Flag
0: can move (can have children)
1: goal
-1: dead end
"""

POD_NAMES = {1:"A1", 2:"A2", 3:"B1", 4:"B2", 5:"C1", 6:"C2", 7:"D1", 8:"D2"}

class Node:

    def __init__(self, state):
        self.state = np.array(state)
        self.next = []

        done = True
        for pos in np.where(self.state != 0)[0]:
            who = self.state[pos]
            if not is_amphipod_done(who, pos):
                done = False
                break
        self.done = done

    def add(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"State: {self.state}"

    def __eq__(self, node2):
        return np.all(self.state == node2.state)

    def __hash__(self):
        return hash("".join(map(str, self.state)))

    def __lt__(self, other):
        return self.energy < other.energy

    def __le__(self, other):
        return self.energy <= other.energy

    def __gt__(self, other):
        return self.energy > other.energy

    def __ge__(self, other):
        return self.energy >= other.energy


class EnergizedNode:
    def __init__(self, node, energy):
        self.node = node
        self.energy = energy

    def __eq__(self, other):
        return self.energy == other.energy

    def __lt__(self, other):
        return self.energy < other.energy

    def __le__(self, other):
        return self.energy <= other.energy

    def __gt__(self, other):
        return self.energy > other.energy

    def __ge__(self, other):
        return self.energy >= other.energy



def is_amphipod_done(who, position):
    a = (who == 1 or who == 2) and (position == 7 or position == 8)
    b = (who == 3 or who == 4) and (position == 9 or position == 10)
    c = (who == 5 or who == 6) and (position == 11 or position == 12)
    d = (who == 7 or who == 8) and (position == 13 or position == 14)
    return a or b or c or d


def are_rooms_done(s):
    done_rooms = np.array([False] * 15)
    if (s[7] == 1 or s[7] == 2) and (s[8] == 1 or s[8] == 2):
        done_rooms[7:9] = True
    if (s[9] == 3 or s[9] == 4) and (s[10] == 3 or s[10] == 4):
        done_rooms[9:11] = True
    if (s[11] == 5 or s[11] == 6) and (s[12] == 5 or s[12] == 6):
        done_rooms[11:13] = True
    if (s[13] == 7 or s[13] == 8) and (s[14] == 7 or s[14] == 8):
        done_rooms[13:15] = True
    return done_rooms


def generate_graph():
    G = {
            0:{1:1}, 1:{0:1,2:2,7:2}, 2:{1:2,3:2,7:2,9:2},
            3:{2:2,4:2,9:2,11:2}, 4:{3:2,5:2,11:2,13:2},
            5:{4:2,6:1,13:2}, 6:{5:1},
            7:{1:2,2:2,8:1}, 8:{7:1},
            9:{2:2,3:2,10:1}, 10:{9:1},
            11:{3:2,4:2,12:1}, 12:{11:1},
            13:{4:2,5:2,14:1}, 14:{13:1},
            }
    return G


def dijkstra(s, t, G):
    dists = np.array([1000] * 15)
    prevs = [None] * 15
    dists[s] = 0
    Q = list(range(15))

    while Q:
        dmin = dists[Q[0]]
        imin = None
        for u in Q:
            if dists[u] <= dmin:
                dmin = dists[u]
                imin = u
        u = imin
        Q.remove(u)

        if u == t:
            break

        for v in G[u].keys():
            if v not in Q:
                continue
            alt = dists[u] + 1
            if alt < dists[v]:
                dists[v] = alt
                prevs[v] = u

    path = [t]
    while path[-1] is not None:
        path.append(prevs[path[-1]])

    path.reverse()
    path.pop(0)
    return path


def generate_shortest_paths(G):
    paths = {}
    for start in range(15):
        for finish in range(15):
            if finish == start:
                continue
            path = dijkstra(start, finish, G)
            print(start, finish, path)
            if start in paths:
                paths[start][finish] = path
            else:
                paths[start] = {finish:path}
    return paths

def is_edge_valid(who, v, w):
    """who is moving from v to w, is it valid?"""
    from_room = v >= 7
    if from_room:
        return True

    if who <= 2:
        return w not in [9, 10, 11, 12, 13, 14]
    elif who <= 4:
        return w not in [7, 8, 11, 12, 13, 14]
    elif who <= 6:
        return w not in [7, 8, 9, 10, 13, 14]
    elif who <= 8:
        return w not in [7, 8, 9, 10, 11, 12]
    else:
        raise ValueError


def generate_paths_(who, start, G):
    paths = []
    def dfs(node, G, visited, reached, current_path):
        visited.add(node)
        current_path.append(node)
        if node not in reached:
            paths.append(current_path.copy())
            reached.add(node)
        for nei in G[node].keys():
            if nei not in current_path and is_edge_valid(who, node, nei):
                dfs(nei, G, visited, reached, current_path)
        current_path.pop(-1)

    reached = set()
    visited = set()
    current_path = []
    dfs(start, G, visited, reached, current_path)

    return paths


def generate_paths(who, start, G, P):
    paths = []
    shortest_paths = P[start]
    for finish, path in shortest_paths.items():
        paths.append(path)
    return paths


def compute_energy(who, path, G):
    coeffs = [1, 1, 10, 10, 100, 100, 1000, 1000]
    coeff = coeffs[who - 1]
    energy = 0
    for v, w in zip(path[:-1], path[1:]):
        cost = G[v][w]
        energy += cost *coeff
    return energy


def compute_remaining(state, P):
    start_positions = np.where(state > 0)[0]
    H = 0
    for start in start_positions:
        who = state[start]
        if who <= 2:
            H += len(P[who][7]) * 1
        elif who <= 4:
            H += len(P[who][9]) * 10
        elif who <= 6:
            H += len(P[who][11]) * 100
        elif who <= 8:
            H += len(P[who][13]) * 1000
    return H


def generate_neighbors(node1, G, P, who_moved):
    state1 = node1.state
    rooms_done = are_rooms_done(state1)

    neighbors = {}

    start_positions = np.where(state1 > 0)[0]
    for start in start_positions:
        from_room = start >= 7
        from_hallway = start <= 6 
        who = state1[start]

        if who in who_moved:
            continue

        if from_room and rooms_done[start]:
            continue

        paths = generate_paths(who, start, G, P)
        possible_paths = []
        for i, path in enumerate(paths):
            to_room = path[-1] >= 7
            to_hallway = path[-1] <= 6
            if from_hallway and to_hallway:
                continue
            if all([state1[v] == 0 for v in path[1:]]):
                possible_paths.append(path)
                #print(f"amphipod {who} {POD_NAMES[who]}'s choice {i}: {path}")

        for path in possible_paths:
            #delta_energy = compute_energy(who, path, G)
            delta_energy = 1
            state2 = np.array(state1)
            state2[path[0]] = 0
            state2[path[-1]] = who
            #H = compute_remaining(state2, P)
            nei = Node(state2)
            neighbors[nei] = delta_energy

    return neighbors


def retrieve_who_moved(u, prevs):
    states = [u]
    while states[-1] is not None:
        states.append(prevs[states[-1]])
    states.reverse()
    states.pop(0)

    who_moved = []
    for v, w in zip(states[:-1], states[1:]):
        i1, i2 = np.where(v.state != w.state)[0]
        if w.state[i1] == 0:
            who = v.state[i1]
        elif w.state[i2] == 0:
            who = v.state[i2]
        who_moved.append(who)

    return who_moved


def step(nodes, G):
    children = []
    for node in nodes:
        children_ = generate_children(node, G)
        children.extend(children_)

    child_best = children[0]
    for child in children:
        if child.energy < child_best.energy:
            child_best = child

    print("best: ", child_best)
    return children


def main(filename):
    G = generate_graph()
    P = generate_shortest_paths(G)

    state0 = [0,0,0,0,0,0,0,3,1,5,7,4,6,8,2]
    state0 = [0,0,0,0,0,0,0,3,1,5,7,4,6,8,2]
    node = Node(state0)

    """
    neighbors = generate_neighbors(node, G, P)
    for nei, de in neighbors.items():
        print(nei, de)
    """

    energies = {node: 0}
    prevs = {node: None}
    Q = [EnergizedNode(node, 0)]
    removed = set()

    count = 0
    while Q:
        count += 1
        u_ene = heapq.heappop(Q)
        u = u_ene.node
        u_energy = u_ene.energy

        removed.add(u)
        print("visiting ", u_energy, u)

        if u.done:
            print("done", u, u_energy)
            break

        who_moved = retrieve_who_moved(u, prevs)
        print("who_moved ", who_moved)
        neighbors = generate_neighbors(u, G, P, who_moved)
        for nei, delta_energy in neighbors.items():
            if nei in removed:
                continue

            alt = u_energy + delta_energy
            heapq.heappush(Q, EnergizedNode(nei, alt))

            if nei not in energies:
                nei_energy = 1e16
            else:
                nei_energy = energies[nei]
            if alt < nei_energy:
                energies[nei] = alt
                prevs[nei] = u

        continue
        for en in Q:
            print(en.energy, en.node)


if __name__ == "__main__":
    main("input.txt")
