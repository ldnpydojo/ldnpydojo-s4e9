

maze = """
1111111111
1        1
1 1       1
1        1
1        1
1   1     1
1        1
1        1
1     1   1
1        1
1111111111
""".strip()

import math
from math import sin, cos
import pyglet
import itertools
import pyglet.window
from pyglet.gl import *
from pyglet.window import key


def itercells():
    for z, l in enumerate(maze.splitlines()):
        for x, c in enumerate(l):
            yield (x, z, c)


def draw_face(p1, p2):
    x1, z1 = p1
    x2, z2 = p2
    dx = x2 - x1
    dz = z2 - z1
    glNormal3f(dz, 0, -dx)
    glBegin(GL_QUADS)
    glVertex3f(x1, 0, z1)
    glVertex3f(x1, 1, z1)
    glVertex3f(x2, 1, z2)
    glVertex3f(x2, 0, z2)
    glEnd()


def draw_block(x, z):
    bl = x - 0.5, z + 0.5
    br = x + 0.5, z + 0.5
    tl = x - 0.5, z - 0.5
    tr = x + 0.5, z - 0.5
    glColor3f(1, 0, 0)
    draw_face(bl, br)
    glColor3f(1, 1, 0)
    draw_face(br, tr)
    glColor3f(0, 1, 0)
    draw_face(tr, tl)
    glColor3f(0, 0, 1)
    draw_face(tl, bl)


pos = (5, 0.5, 5)
ang = 0
tang = 0


def get_dir():
    return sin(ang), 0, cos(ang)


def on_draw():
    glClearColor(0, 0, 0.2, 0)
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 800 / 600.0, 0.01, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    x, y, z = pos
    look_at = x + sin(ang), y, z + cos(ang)
    gluLookAt(*itertools.chain(
        (x, y, z),
        look_at,
        (0, 1, 0)
    ))
    #glEnable(GL_LIGHTING)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_GREATER)

    #glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat * 3)(5, 0.5, 5))

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    for x, z, block in itercells():
        if block == '1':
            draw_block(x, z)


def on_key_press(symbol, modifiers):
    global tang, pos
    if symbol == key.LEFT:
        print "left"
        tang += math.pi * 0.5
    elif symbol == key.RIGHT:
        print "right"
        tang -= math.pi * 0.5
    elif symbol == key.UP:
        x, y, z = pos
        dx, dy, dz = get_dir()
        pos = x + dx, y + dy, z + dz


def update(dt):
    global ang
    ang = ang - (ang - tang) * 0.1 ** dt


if __name__ == '__main__':
    window = pyglet.window.Window(
        width=800,
        height=600
    )

    window.event(on_draw)
    window.event(on_key_press)
    pyglet.clock.schedule_interval(update, 1.0 / 30)
    pyglet.app.run()
