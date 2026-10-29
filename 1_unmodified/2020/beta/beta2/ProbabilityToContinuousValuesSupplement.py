# ==============================================================================
# Scene:      ProbabilityToContinuousValuesSupplement
# Source:     videos/_2020/beta/beta2.py (lines 609-660)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProbabilityToContinuousValuesSupplement.py ProbabilityToContinuousValuesSupplement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProbabilityToContinuousValuesSupplement(Scene):
    def construct(self):
        nl = UnitInterval()
        nl.set_width(10)
        nl.add_numbers(
            *np.arange(0, 1.1, 0.1),
            buff=0.3,
        )
        nl.to_edge(LEFT)
        self.add(nl)

        def f(x):
            return -100 * (x - 0.6) * (x - 0.8)

        values = np.linspace(0.65, 0.75, 100)
        lines = VGroup()
        for x, color in zip(values, it.cycle([BLUE_E, BLUE_C])):
            line = Line(ORIGIN, UP)
            line.set_height(f(x))
            line.set_stroke(color, 1)
            line.move_to(nl.n2p(x), DOWN)
            lines.add(line)

        self.play(ShowCreation(lines, lag_ratio=0.9, run_time=5))

        lines_row = lines.copy()
        lines_row.generate_target()
        for lt in lines_row.target:
            lt.rotate(90 * DEGREES)
        lines_row.target.arrange(RIGHT, buff=0)
        lines_row.target.set_stroke(width=4)
        lines_row.target.next_to(nl, UP, LARGE_BUFF)
        lines_row.target.align_to(nl.n2p(0), LEFT)

        self.play(
            MoveToTarget(
                lines_row,
                lag_ratio=0.1,
                rate_func=rush_into,
                run_time=4,
            )
        )
        self.wait()
        self.play(
            lines.set_height, 0.01, {"about_edge": DOWN, "stretch": True},
            ApplyMethod(
                lines_row.set_width, 0.01, {"about_edge": LEFT},
                rate_func=rush_into,
            ),
            run_time=6,
        )
        self.wait()
