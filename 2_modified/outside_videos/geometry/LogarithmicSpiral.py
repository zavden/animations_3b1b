# ==============================================================================
# Scene:      LogarithmicSpiral
# Source:     videos/outside_videos/geometry.py (lines 153-203)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LogarithmicSpiral.py LogarithmicSpiral -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - old syntax self.play(mob.method, args) -> mob.animate.method(args)
# ==============================================================================

from manim_imports_ext import *

class LogarithmicSpiral(Scene):
    def construct(self):
        exp_n_tracker = ValueTracker(1)
        group = VGroup()

        def update_group(gr):
            n = 3 * int(np.exp(exp_n_tracker.get_value()))
            gr.set_submobjects(self.get_group(n))

        group.add_updater(update_group)

        self.add(group)
        # CHANGE: old syntax self.play(mob.method, args) -> mob.animate.method(args)
        self.play(
            exp_n_tracker.animate.set_value(7),
            run_time=10,
            rate_func=linear,
        )
        self.wait()

    def get_group(self, n, n_spirals=50):
        n = int(n)
        theta = TAU / n
        R = 10

        lines = VGroup(*[
            VMobject().set_points_as_corners([ORIGIN, R * v])
            for v in compass_directions(n)
        ])
        lines.set_stroke(WHITE, min(1, 25 / n))

        # points = [3 * RIGHT]
        # transform = np.array(rotation_matrix_transpose(90 * DEGREES + theta, OUT))
        # transform *= math.sin(theta)
        points = [RIGHT]
        transform = np.array(rotation_matrix_transpose(90 * DEGREES, OUT))
        transform *= math.tan(theta)

        for x in range(n_spirals * n):
            p = points[-1]
            dp = np.dot(p, transform)
            points.append(p + dp)

        vmob = VMobject()
        vmob.set_points_as_corners(points)

        vmob.scale(math.tan(theta), about_point=ORIGIN)

        vmob.set_stroke(BLUE, clip(1000 / n, 1, 3))

        return VGroup(lines, vmob)
