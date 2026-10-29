# ==============================================================================
# Scene:      NoClearCutPath
# Source:     videos/_2019/QA_2to21.py (lines 77-158)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NoClearCutPath.py NoClearCutPath -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use the Cairo signature of smooth(t, inflection), keeping the one-argument call.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import cairo_smooth as smooth

class NoClearCutPath(Scene):
    def construct(self):
        path1 = VMobject()
        path1.start_new_path(3 * LEFT)
        path1.add_line_to(ORIGIN)
        path1.append_points([
            ORIGIN,
            2.5 * RIGHT,
            2.5 * RIGHT + 3 * UP,
            5 * RIGHT + 3 * UP,
        ])
        path2 = path1.copy()
        path2.rotate(PI, axis=RIGHT, about_point=ORIGIN)
        paths = VGroup(path1, path2)
        paths.to_edge(LEFT)
        paths.set_stroke(WHITE, 2)

        labels = VGroup(
            OldTexText("Pure mathematicians"),
            OldTexText("Applied mathematicians"),
        )
        for label, path in zip(labels, paths):
            label.next_to(path.get_end(), RIGHT)

        animations = []
        n_animations = 20
        colors = [BLUE_C, BLUE_D, BLUE_E, GREY_BROWN]
        for x in range(n_animations):
            dot = self.get_dot(random.choice(colors))
            path = random.choice(paths)
            dot.move_to(path.get_start())
            anim = Succession(
                # FadeIn(dot),
                MoveAlongPath(dot, path, run_time=4, rate_func=lambda t: smooth(t, 2)),
                FadeOut(dot),
            )
            animations.append(anim)

        alt_path = VMobject()
        alt_path.start_new_path(paths.get_left())
        alt_path.add_line_to(paths.get_left() + 3 * RIGHT)
        alt_path.add_line_to(2 * UP)
        alt_path.add_line_to(2 * DOWN + RIGHT)
        alt_path.add_line_to(2 * RIGHT)
        alt_path.add_line_to(3 * RIGHT)
        alt_path.add_line_to(8 * RIGHT)
        alt_path.make_smooth()
        alt_path.set_stroke(YELLOW, 3)
        dashed_path = DashedVMobject(alt_path, num_dashes=100)

        alt_dot = self.get_dot(YELLOW)
        alt_dot.move_to(alt_path.get_start())
        alt_dot_anim = MoveAlongPath(
            alt_dot,
            alt_path,
            run_time=10,
            rate_func=linear,
        )

        self.add(paths)
        self.add(labels)
        self.play(
            LaggedStart(
                *animations,
                run_time=10,
                lag_ratio=1 / n_animations,
            ),
            ShowCreation(
                dashed_path,
                rate_func=linear,
                run_time=10,
            ),
            alt_dot_anim,
        )
        self.wait()

    def get_dot(self, color):
        dot = Dot()
        dot.scale(1.5)
        dot.set_color(color)
        dot.set_stroke(BLACK, 2, background=True)
        return dot
