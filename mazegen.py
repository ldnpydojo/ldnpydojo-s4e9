#!/usr/bin/env python3
from __future__ import print_function
import random
import time
from itertools import product


class Grid(object):
    @staticmethod
    def itercoords(size):
        """Iterate through all coordinates of a grid of size x size."""
        return product(
            range(size),
            range(size)
        )

    def __init__(self, size, values):
        self.size = size
        self.values = values

    def __getitem__(self, pos):
        return pos in self.values

    def __contains__(self, pos):
        gs = self.size - 1
        return all(0 < c < gs for c in pos)

    def set(self, pos):
        self.values.add(pos)

    def clear(self, pos):
        self.values.discard(pos)

    def __str__(self):
        o = []
        for y in range(self.size):
            o.append(
                ''.join(' #'[int(self[x, y])] for x in range(self.size))
            )
        return '\n'.join(o)


DIRECTIONS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]



def _valid_directions(grid, x, y):
    for dx, dy in DIRECTIONS:
        p = x + dx, y + dy

        # Not usable if out of bounds
        if p not in grid:
            continue

        yield p


def _usable_directions(grid, x, y):
    for p in _valid_directions(grid, x, y):
        # Not usable if already taken
        if not grid[p]:
            continue

        # Not usable if would connect
        for p2 in _valid_directions(grid, *p):
            # If already taken, would connect
            if p2 != (x, y) and not grid[p2]:
                break
        else:
            yield p


START = 1, 1


def generate_maze(size, animate=False):
    s = set()
    for x, y in Grid.itercoords(size):
        s.add((x, y))
    g = Grid(size, s)
    stack = []
    p = START
    while True:
        g.clear(p)
        x, y = p
        dirs = list(_usable_directions(g, x, y))
        if not dirs:
            try:
                p = stack.pop()
            except IndexError:
                break
            else:
                continue
        stack.append(p)
        p = random.choice(dirs)
        if animate:
            print(g)
            print()
            time.sleep(0.1)
    return g


if __name__ == '__main__':
    m = generate_maze(20, animate=True)
    print(m)
