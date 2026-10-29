# ==============================================================================
# Scene:      SumRotVectors
# Source:     videos/outside_videos/analysis.py (lines 222-257)
# Category:   2 · Renders with modifications
# Includes code copied from: _2016/zeta.py
#
# Run from this folder:
#     manimgl SumRotVectors.py SumRotVectors -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - old syntax self.play(mob.method, args) -> mob.animate.method(args)
# ==============================================================================

from manim_imports_ext import *
import mpmath


# ----- From _2016/zeta.py -----

mpmath.mp.dps = 7



# ----- From outside_videos/analysis.py -----

class SumRotVectors(Scene):
    CONFIG = {
        "n_vects": 100,
    }

    def construct(self):
        plane = ComplexPlane()
        circle = Circle(color=YELLOW)

        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        vects = always_redraw(lambda: self.get_vects(get_t()))

        self.add(plane, circle)
        self.add(t_tracker, vects)
        # CHANGE: old syntax self.play(mob.method, args) -> mob.animate.method(args)
        self.play(
            t_tracker.animate.set_value(1),
            run_time=10,
            rate_func=linear,
        )
        self.play(ShowIncreasingSubsets(vects, run_time=5))

    def get_vects(self, t):
        vects = VGroup()
        last_tip = ORIGIN
        for n in range(self.n_vects):
            vect = Vector(RIGHT)
            vect.rotate(n * TAU * t, about_point=ORIGIN)
            vect.shift(last_tip)
            last_tip = vect.get_end()
            vects.add(vect)

        vects.set_submobject_colors_by_gradient(BLUE, GREEN, YELLOW, RED)
        vects.set_opacity(0.5)
        return vects
