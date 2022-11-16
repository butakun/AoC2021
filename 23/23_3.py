#!/usr/bin/env python3

import pathlib
import sys

from functools import total_ordering
from queue import PriorityQueue
from typing import Dict, List, Tuple

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

import aoc


Amphipod = Tuple[str, int, int]
Grid = Dict[Tuple[int, int], str]

@total_ordering
class Burrow:
  def __init__(self, grid: Grid, energy: int = 0) -> None:
    self.grid = grid
    self.energy = energy
    self.depth = max(y for x, y in self.grid if self.grid[x, y] != "#")

  def __str__(self) -> str:
    return "\n".join("".join(self.grid.get((x, y), ' ') for x in range(13)) for y in range(self.depth + 2))

  def __eq__(self, other: 'Burrow') -> bool:
    return self.energy == other.energy and self.distance() == other.distance()

  def __lt__(self, other: 'Burrow') -> bool:
    return self.energy < other.energy

  def copy(self) -> 'Burrow':
    return Burrow(self.grid.copy(), self.energy)

  def unfold(self) -> 'Burrow':
    grid = self.grid.copy()
    for x, y in self.grid.keys():
      if y >= 3:
        grid[x, y + 2] = self.grid[x, y]

    grid[3, 3] = 'D'
    grid[5, 3] = 'C'
    grid[7, 3] = 'B'
    grid[9, 3] = 'A'
    grid[3, 4] = 'D'
    grid[5, 4] = 'B'
    grid[7, 4] = 'A'
    grid[9, 4] = 'C'

    return Burrow(grid, self.energy)

  def pods(self) -> List[Amphipod]:
    return [(t, x, y) for (x, y), t in self.grid.items() if t not in {"#", "."}]

  def homed(self) -> int:
    return sum(int(self.is_home(pod)) for pod in self.pods())

  def state(self) -> str:
    return ",".join(f'{k}:{v}' for k, v in self.grid.items())

  def is_home(self, pod: Amphipod) -> bool:
    t, x, y = pod

    if 3 + (ord(t) - ord('A')) * 2 != x:
      return False

    for by in range(self.depth, y, -1):
      if self.grid[x, by] != t:
        return False

    return True

  def resolve(self) -> int:
    seen = {}

    q = PriorityQueue(-1)
    q.put(self)

    while not q.empty():
      burrow = q.get()

      if burrow.homed() == 4 * (self.depth - 1):
        break

      state = burrow.state()
      if state in seen and seen[state] <= burrow.energy:
        continue

      seen[state] = burrow.energy

      for pod in burrow.pods():
        if burrow.is_home(pod):
          continue
  
        burrows = burrow.moves(pod)
        for new_burrow in burrows:
          q.put(new_burrow)

    return burrow.energy, burrow

  def moves(self, pod: Amphipod) -> List['Burrow']:
    t, x, y = pod

    dests = {(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1), (11, 1)} if y > 1 else set()

    room_x = {'A': 3, 'B': 5, 'C': 7, 'D': 9}[t]
    for room_y in range(self.depth, 1, -1):
      if self.grid[room_x, room_y] == '.':
        dests.add((room_x, room_y))
      elif self.grid[room_x, room_y] != t:
        break
  
    seen = set()
    stack = [(x, y)]
    moves = []

    while stack:
      nx, ny = stack.pop()
      seen.add((nx, ny))

      for dx, dy in ((nx - 1, ny), (nx + 1, ny), (nx, ny + 1), (nx, ny - 1)):
        if (dx, dy) not in self.grid or (dx, dy) in seen or self.grid[dx, dy] != '.':
          continue

        stack.append((dx, dy))

        if (dx, dy) in dests:
          burrow = self.copy()
          burrow.energy += (abs(x - dx) + abs(1 - y) + abs(1 - dy)) * (10 ** (ord(t) - ord('A')))
          burrow.grid[dx, dy], burrow.grid[x, y] = self.grid[x, y], self.grid[dx, dy]
          moves.append(burrow)

    return moves


def read_input() -> Burrow:
  grid = {}
  lines = [line.rstrip() for line in open(aoc.inputfile('input.txt')).readlines()]
  for y, line in enumerate(lines):
     wall_seen = False
     for x, c in enumerate(line):
       if c == " ": continue
       grid[x, y] = c

  return Burrow(grid)


def run() -> None:
  burrow = read_input()
  energy, solution = burrow.resolve()
  print(f'Minimum energy required: {energy}')
  print(f'{solution}')

  burrow = burrow.unfold()
  energy, solution = burrow.resolve()
  print(f'Minimum energy required (unfolded): {energy}')
  print(f'{solution}')


if __name__ == '__main__':
  run()
  sys.exit(0)
