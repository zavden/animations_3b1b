# ==============================================================================
# Scene:      ReedSolomonPreview
# Source:     videos/_2020/hamming.py (lines 6057-6140)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ReedSolomonPreview.py ReedSolomonPreview -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - self.mobjects includes mobjects that are not VMobjects; VGroup fails, Group is used
# ==============================================================================

from manim_imports_ext import *

class ReedSolomonPreview(Scene):
    def construct(self):
        # Setup
        title = OldTexText("Reed-Solomon basic idea")
        title.set_height(0.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        axes = Axes(
            x_range=(-1, 10, 1), y_range=(-1, 8, 1),
            width=12,
            height=7,
        )
        axes.to_edge(DOWN, buff=SMALL_BUFF)
        axes.set_color(GREY_B)

        cubic = axes.get_graph(
            lambda x: -0.05 * x * (x - 2) * (x - 4) * (x - 8) + 2
        )
        cubic.set_stroke(TEAL, 3)

        self.add(title)
        self.add(axes)

        # Data
        dots = VGroup(*[
            Dot(axes.input_to_graph_point(x, cubic))
            for x in range(0, 8)
        ])
        dots[:4].set_color(YELLOW)
        dots[4:].set_color(BLUE)

        # Input words
        input_words = OldTexText("Input data")
        poly_words = OldTexText("Polynomial\\\\fit")
        redundant_words = OldTexText("Redundancy")

        input_words.next_to(dots[:4], UP, buff=2)
        input_words.set_color(YELLOW)
        input_arrows = VGroup(*[
            Arrow(input_words.get_bottom(), dot.get_center())
            for dot in dots[:4]
        ])
        input_arrows.set_fill(YELLOW)

        poly_words.next_to(dots[5], LEFT)
        poly_words.shift(0.5 * UR)
        poly_words.match_color(cubic)

        redundant_words.move_to(dots[4:].get_center(), LEFT)
        redundant_words.shift(2 * DR + DOWN)
        redundant_words.set_color(BLUE)
        redundant_arrows = VGroup(*[
            Arrow(redundant_words.get_corner(UL), dot.get_center())
            for dot in dots[4:]
        ])
        redundant_arrows.set_color(BLUE)

        # Animations
        kw = {"lag_ratio": 0.5}
        self.play(
            FadeIn(input_words),
            LaggedStartMap(FadeIn, dots[:4], lambda m: (m, UP), **kw),
            LaggedStartMap(GrowArrow, input_arrows, **kw),
        )
        self.add(cubic, *dots[:4])
        self.play(
            ShowCreation(cubic),
            Write(poly_words)
        )
        self.wait()
        self.play(
            FadeIn(redundant_words),
            LaggedStartMap(FadeIn, dots[4:], lambda m: (m, DR), **kw),
            LaggedStartMap(GrowArrow, redundant_arrows, **kw),
        )
        self.wait()

        self.play(LaggedStartMap(
            # CHANGE: self.mobjects includes mobjects that are not VMobjects; VGroup fails, Group is used
            FadeOut, Group(*reversed(self.mobjects)),
            lambda m: (m, 0.2 * normalize(m.get_center())),
            lag_ratio=0.1,
            run_time=2,
        ))
        self.wait()
