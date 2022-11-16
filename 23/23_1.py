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

    def __init__(self, state, energy=0, parent=None):
        self.state = np.array(state)
        self.energy = energy
        self.children = []
        self.parent = parent
        self.last_moved = -1

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
        return f"State: {self.state}, Energy: {self.energy}, Done: {self.done}"

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


def is_move_allowed(state1, state2):
    """ can node1 transition to node2? """
    imoved = np.where(state1 != state2)[0]
    who_moved = -1
    if state2[imoved[0]] != 0:
        who_moved = state1[imoved[0]]
        start  = imoved[1]
        finish = imoved[0]
    else:
        who_moved = state2[imoved[1]]
        start  = imoved[0]
        finish = imoved[1]

    assert state1[start] == who_moved

    possible = [True] * 15


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


def generate_paths(who, start, G):
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


def compute_energy(who, path, G):
    coeffs = [1, 1, 10, 10, 100, 100, 1000, 1000]
    coeff = coeffs[who - 1]
    energy = 0
    for v, w in zip(path[:-1], path[1:]):
        cost = G[v][w]
        energy += cost *coeff
    return energy


def generate_children(node1, G):
    state1 = node1.state
    children = []
    rooms_done = are_rooms_done(state1)

    start_positions = np.where(state1 > 0)[0]
    for start in start_positions:
        from_room = start >= 7
        from_hallway = start <= 6 
        who = state1[start]

        if from_room and rooms_done[start]:
            continue

        if who == node1.last_moved:
            continue

        paths = generate_paths(who, start, G)
        possible_paths = []
        for i, path in enumerate(paths):
            to_room = path[-1] >= 7
            to_hallway = path[-1] <= 6
            if from_hallway and to_hallway:
                continue
            if state1[path[-1]] != 0:
                continue
            if all([state1[v] == 0 for v in path[1:-1]]):
                possible_paths.append(path)
                #print(f"amphipod {who} {POD_NAMES[who]}'s choice {i}: {path}")

        for path in possible_paths:
            state2 = np.array(state1)
            state2[path[0]] = 0
            state2[path[-1]] = who
            de = compute_energy(who, path, G)
            child = Node(state2, node1.energy+de, node1)
            child.last_moved = who
            children.append(child)

    return children


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

    state0 = [0,0,0,0,0,0,0,3,1,5,7,4,6,8,2]
    node = Node(state0)

    tried = set()
    children = generate_children(node, G)
    stack = children.copy()

    best = None
    while stack:
        #u = heapq.heappop(stack)
        u = stack.pop(0)
        print("stack size = ", len(stack), len(tried), "best = ", best)
        print(u)
        tried.add(u)
        children = generate_children(u, G)
        print("children = ")
        for c in children:
            print(c)

        if u.done:
            if best is None:
                best = u
            elif u < best:
                best = u

        if False:
            for child in children:
                heapq.heappush(stack, child)
        else:
            stack.extend(children)

if __name__ == "__main__":
    main("input.txt")
