# ==============================================================================
# Scene:      ExpDeriv
# Source:     videos/_2025/laplace/main_equations.py (lines 632-669)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpDeriv.py ExpDeriv -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpDeriv(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"{t}": BLUE, "{s}": YELLOW}
        lhs, rhs = terms = VGroup(
            Tex(tex, t2c=t2c, font_size=90)
            for tex in [R"e^{{s}{t}}", R"{s} e^{{s}{t}}"]
        )
        terms.arrange(RIGHT, buff=4)

        arrows = VGroup(
            Arrow(
                lhs.get_corner(sign * UP + RIGHT),
                rhs.get_corner(sign * UP + LEFT),
                path_arc=-sign * 75 * DEG,
                thickness=4
            )
            for sign in [1, -1]
        )
        arrows.set_fill(border_width=2)
        arrows[1].shift(0.25 * DOWN)
        arrow_labels = VGroup(
            Tex(tex, t2c=t2c, font_size=60).next_to(arrow, vect)
            for arrow, tex, vect in zip(arrows, ["d / d{t}", R"\times {s}"], [UP, DOWN])
        )
        self.add(terms[0])
        self.play(
            TransformFromCopy(terms[0].copy(), terms[1][1:], path_arc=-75 * DEG),
            Write(arrows[0], time_span=(0.5, 1.5)),
            FadeIn(arrow_labels[0], lag_ratio=0.1),
            run_time=1.5,
        )
        self.play(FadeTransform(terms[1][2].copy(), terms[1][0], path_arc=90 * DEG, run_time=0.75))
        self.play(LaggedStart(
            TransformFromCopy(*arrows),
            TransformFromCopy(*arrow_labels),
        ))
        self.wait(2)
