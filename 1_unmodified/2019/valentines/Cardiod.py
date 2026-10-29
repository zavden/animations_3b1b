# ==============================================================================
# Scene:      Cardiod
# Source:     videos/_2019/valentines.py (lines 94-135)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Cardiod.py Cardiod -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Cardiod(Scene):
    def construct(self):
        r = 1
        big_circle = Circle(color=BLUE, radius=r)
        big_circle.set_stroke(width=1)
        big_circle.rotate(-PI / 2)
        time_tracker = ValueTracker()
        get_time = time_tracker.get_value

        def get_lil_circle():
            lil_circle = big_circle.copy()
            lil_circle.set_color(YELLOW)
            time = get_time()
            lil_circle.rotate(time)
            angle = 0.5 * time
            lil_circle.shift(
                rotate_vector(UP, angle) * 2 * r
            )
            return lil_circle
        lil_circle = always_redraw(get_lil_circle)

        cardiod = ParametricCurve(
            lambda t: op.add(
                rotate_vector(UP, 0.5 * t) * (2 * r),
                -rotate_vector(UP, 1.0 * t) * r,
            ),
            t_min=0,
            t_max=(2 * TAU),
        )
        cardiod.set_color(MAROON_B)

        dot = Dot(color=RED)
        dot.add_updater(lambda m: m.move_to(lil_circle.get_start()))

        self.add(big_circle, lil_circle, dot, cardiod)
        for color in [RED, PINK, MAROON_B]:
            self.play(
                ShowCreation(cardiod.copy().set_color(color)),
                time_tracker.increment_value, TAU * 2,
                rate_func=linear,
                run_time=6,
            )
