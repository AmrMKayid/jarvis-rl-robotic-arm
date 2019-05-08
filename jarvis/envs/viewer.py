import pyglet
import numpy as np


class Viewer(pyglet.window.Window):
    bar_thickness = 5

    def __init__(self, arm_info, goal):
        super(Viewer, self).__init__(width=400, height=400,
                                     resizable=False, caption='Jarvis Arm', vsync=False)
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.arm_info = arm_info
        self.center_coord = np.array([200, 200])

        # display whole batch at once
        self.batch = pyglet.graphics.Batch()

        self.goal = self.batch.add(
            4, pyglet.gl.GL_QUADS, None,    # 4 corners
            # location
            ('v2f', [goal['x'] - goal['l'] / 2, goal['y'] - goal['l'] / 2,
                     goal['x'] - goal['l'] / 2, goal['y'] + goal['l'] / 2,
                     goal['x'] + goal['l'] / 2, goal['y'] + goal['l'] / 2,
                     goal['x'] + goal['l'] / 2, goal['y'] - goal['l'] / 2]),
            # color
            ('c3B', (86, 109, 249) * 4))

        self.arm1 = self.batch.add(
            4, pyglet.gl.GL_QUADS, None,
            ('v2f', [250, 250,
                     250, 300,
                     260, 300,
                     260, 250]),
            ('c3B', (249, 86, 86) * 4,))

        self.arm2 = self.batch.add(
            4, pyglet.gl.GL_QUADS, None,
            ('v2f', [100, 150,
                     100, 160,
                     200, 160,
                     200, 150]),
            ('c3B', (249, 86, 86) * 4,))

    def render(self):
        self._update_arm()
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def _update_arm(self):
        (a1l, a2l) = self.arm_info['l']     # radius, arm length
        (a1r, a2r) = self.arm_info['r']     # radian, angle
        a1xy = self.center_coord            # a1 start (x0, y0)
        a1xy_ = np.array([np.cos(a1r), np.sin(a1r)]) * a1l + \
            a1xy   # a1 end and a2 start (x1, y1)
        a2xy_ = np.array([np.cos(a1r+a2r), np.sin(a1r+a2r)]
                         ) * a2l + a1xy_  # a2 end (x2, y2)

        a1tr, a2tr = np.pi / 2 - \
            self.arm_info['r'][0], np.pi / 2 - self.arm_info['r'].sum()
        xy01 = a1xy + np.array([-np.cos(a1tr), np.sin(a1tr)]) * self.bar_thickness
        xy02 = a1xy + np.array([np.cos(a1tr), -np.sin(a1tr)]) * self.bar_thickness
        xy11 = a1xy_ + np.array([np.cos(a1tr), -np.sin(a1tr)]) * self.bar_thickness
        xy12 = a1xy_ + np.array([-np.cos(a1tr), np.sin(a1tr)]) * self.bar_thickness

        xy11_ = a1xy_ + np.array([np.cos(a2tr), -np.sin(a2tr)]) * self.bar_thickness
        xy12_ = a1xy_ + np.array([-np.cos(a2tr), np.sin(a2tr)]) * self.bar_thickness
        xy21 = a2xy_ + np.array([-np.cos(a2tr), np.sin(a2tr)]) * self.bar_thickness
        xy22 = a2xy_ + np.array([np.cos(a2tr), -np.sin(a2tr)]) * self.bar_thickness

        self.arm1.vertices = np.concatenate((xy01, xy02, xy11, xy12))
        self.arm2.vertices = np.concatenate((xy11_, xy12_, xy21, xy22))
