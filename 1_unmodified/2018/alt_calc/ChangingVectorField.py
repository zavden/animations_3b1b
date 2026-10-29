# ==============================================================================
# Scene:      ChangingVectorField
# Source:     videos/_2018/alt_calc.py (lines 919-981)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ChangingVectorField.py ChangingVectorField -w -m --fps 15
#
# Notes:
#   Rendered at 854x480, 10 fps (not 720p15): 30 s of 600+ updating vectors took more than 900 s per attempt at 720p15 (timeout). Same scene content.
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class ChangingVectorField(Scene):
    CONFIG = {
        "wait_time": 30,
    }

    def construct(self):
        plane = self.plane = NumberPlane()
        plane.set_stroke(width=2)
        plane.add_coordinates()
        self.add(plane)

        # Obviously a silly thing to do, but I'm sweeping
        # through trying to make sure old scenes don't
        # completely break in spots which used to have
        # Continual animations
        time_tracker = self.time_tracker = ValueTracker(0)
        time_tracker.add_updater(
            lambda t: t.set_value(self.get_time())
        )

        vectors = self.get_vectors()
        vectors.add_updater(self.update_vectors)
        self.add(vectors)
        self.wait(self.wait_time)

    def get_vectors(self):
        vectors = VGroup()
        x_max = int(np.ceil(FRAME_WIDTH))
        y_max = int(np.ceil(FRAME_HEIGHT))
        step = 0.5
        for x in np.arange(-x_max, x_max + 1, step):
            for y in np.arange(-y_max, y_max + 1, step):
                point = x * RIGHT + y * UP
                vectors.add(Vector(RIGHT).shift(point))
        vectors.set_color_by_gradient(YELLOW, RED)
        return vectors

    def update_vectors(self, vectors):
        time = self.time_tracker.get_value()
        for vector in vectors:
            point = vector.get_start()
            out_point = self.func(point, time)
            norm = get_norm(out_point)
            if norm == 0:
                out_point = RIGHT  # Fake it
                vector.set_fill(opacity=0)
            else:
                out_point *= 0.5
                color = interpolate_color(BLUE, RED, norm / np.sqrt(8))
                vector.set_fill(color, opacity=1)
                vector.set_stroke(BLACK, width=1)
            new_x, new_y = out_point[:2]
            vector.put_start_and_end_on(
                point, point + new_x * RIGHT + new_y * UP
            )

    def func(self, point, time):
        x, y, z = point
        return np.array([
            np.sin(time + 0.5 * x + y),
            np.cos(time + 0.2 * x * y + 0.7),
            0
        ])
