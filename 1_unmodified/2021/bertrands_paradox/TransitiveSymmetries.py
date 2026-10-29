# ==============================================================================
# Scene:      TransitiveSymmetries
# Source:     videos/_2021/bertrands_paradox.py (lines 711-747)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TransitiveSymmetries.py TransitiveSymmetries -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TransitiveSymmetries(Scene):
    def construct(self):
        circle = Circle(radius=3)
        circle.set_stroke(GREY_B, 2)
        circle.rotate(PI / 2)

        dots = DotCloud([circle.pfp(a) for a in np.linspace(0, 1, 49)])
        dots.set_glow_factor(5)
        dots.set_radius(0.5)
        dots.set_color(WHITE)
        dots.set_opacity(0.5)

        dot = dots.copy()
        dot.set_points([dots.get_points()[0]])
        dot.set_color(YELLOW)
        dot.set_opacity(1)

        top_words = Text("By acting on any one point...")
        top_words.match_x(dot)
        top_words.to_edge(UP, buff=MED_SMALL_BUFF)
        low_words = Text("...you can map\nto any other")
        low_words.to_edge(RIGHT).shift(2 * DOWN)

        self.add(circle, top_words, dot)
        dots.add_updater(lambda m: m)
        self.play(
            Rotate(
                Group(circle, dot), TAU,
                about_point=circle.get_center(),
            ),
            ShowCreation(
                dots,
                rate_func=lambda a: smooth(a * (1 - 1 / 48) + 1 / 48)
            ),
            Write(low_words, rate_func=squish_rate_func(smooth, 0.3, 0.5)),
            run_time=10,
        )
