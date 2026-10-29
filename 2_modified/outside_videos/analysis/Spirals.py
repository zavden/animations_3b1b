# ==============================================================================
# Scene:      Spirals
# Source:     videos/outside_videos/analysis.py (lines 260-330)
# Category:   2 · Renders with modifications
# Includes code copied from: _2016/zeta.py
#
# Run from this folder:
#     manimgl Spirals.py Spirals -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ComplexValueTracker no longer encodes the value in its position (get_center); get_value is used
#   - old syntax self.play(mob.method, args) -> mob.animate.method(args)
# ==============================================================================

from manim_imports_ext import *
import mpmath


# ----- From _2016/zeta.py -----

mpmath.mp.dps = 7



# ----- From outside_videos/analysis.py -----

class Spirals(Scene):
    CONFIG = {
        "n_lines": 1200
    }

    def construct(self):
        s_tracker = ComplexValueTracker(complex(2, 1))
        get_s = s_tracker.get_value
        spiral = always_redraw(
            lambda: self.get_spiral(get_s())
        )
        s_dot = always_redraw(
            # CHANGE: ComplexValueTracker no longer encodes the value in its position (get_center); get_value is used
            lambda: Dot(complex_to_R3(get_s()), color=YELLOW)
        )
        s_label = always_redraw(
            lambda: DecimalNumber(get_s()).to_corner(UR)
        )

        self.add(ComplexPlane().set_stroke(width=0.5))
        self.add(spiral, s_dot, s_label)
        # CHANGE: old syntax self.play(mob.method, args) -> mob.animate.method(args)
        self.play(s_tracker.animate.set_value(complex(1, 1)), run_time=3)
        sigma = 0.5
        zero_ts = [
            14.134725,
            21.022040,
            25.010858,
            30.424876,
            32.935062,
            37.586178,
        ]
        self.wait()
        # CHANGE: old syntax self.play(mob.method, args) -> mob.animate.method(args)
        self.play(s_tracker.animate.set_value(complex(sigma, 1)), run_time=3)
        self.wait()
        for zero_t in zero_ts:
            # CHANGE: old syntax self.play(mob.method, args) -> mob.animate.method(args)
            self.play(
                s_tracker.animate.set_value(complex(sigma, zero_t)),
                run_time=3,
            )
            updaters = spiral.get_updaters()
            spiral.clear_updaters()
            self.play(FadeOut(spiral))
            self.play(ShowCreation(spiral, run_time=3))
            for updater in updaters:
                spiral.add_updater(updater)
            self.wait()

    def get_spiral(self, s, colors=[RED, BLUE]):
        n_lines = self.n_lines
        lines = VGroup()
        colors = it.cycle(colors)
        for n in range(1, n_lines + 1):
            z = self.n_to_z(n, s, n_lines)
            if abs(z) == 0:
                continue
            line = Line(ORIGIN, complex_to_R3(z))
            line.set_stroke(
                colors.__next__(),
                width=3 * abs(z)**0.1
            )
            if len(lines) > 0:
                line.shift(lines[-1].get_end())
            lines.add(line)
        return lines

    def n_to_z(self, n, s, n_lines):
        # if is_prime(n):
        #     return -np.log(1 - n**(-s))
        # else:
        #     return 0
        # return n**(-s)
        return (n**(-s)) * (n_lines - n) / n_lines
