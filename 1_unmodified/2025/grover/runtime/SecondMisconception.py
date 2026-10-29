# ==============================================================================
# Scene:      SecondMisconception
# Source:     videos/_2025/grover/runtime.py (lines 740-799)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SecondMisconception.py SecondMisconception -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SecondMisconception(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Misconception #2", font_size=90)
        title.to_edge(UP, buff=LARGE_BUFF)
        title.add(Underline(title))
        title.set_color(BLUE)

        words = Text(
            "Quantum Computers would make\n" + \
            "everything exponentially faster",
            font_size=60
        )
        words.next_to(title, DOWN, MED_LARGE_BUFF)
        red_cross = Cross(words["everything"])
        red_cross.set_stroke(RED, [0, 8, 8, 8, 0])
        new_words = Text("some very\nspecial problems", alignment="LEFT")
        new_words.set_color(RED)
        new_words.next_to(red_cross, DOWN, aligned_edge=LEFT)

        self.add(title)
        self.play(Write(words, run_time=2))
        self.wait()
        self.play(LaggedStart(
            ShowCreation(red_cross),
            FadeIn(new_words, lag_ratio=0.1),
            FadeOut(title),
            lag_ratio=0.35
        ))
        self.wait()

        # Show factoring number
        factors = VGroup(Integer(314159), Integer(271829))
        factors.arrange(RIGHT, buff=LARGE_BUFF)
        product = Integer(factors[0].get_value() * factors[1].get_value())
        product.next_to(factors, UP, LARGE_BUFF)
        lines = VGroup(
            Line(product.get_bottom(), factor.get_top(), buff=0.2)
            for factor in factors
        )
        lines.set_submobject_colors_by_gradient(BLUE, GREEN)
        product.set_color(TEAL)
        factors.set_submobject_colors_by_gradient(BLUE, GREEN)
        times = Tex(R"\times")
        times.move_to(factors)

        factor_group = VGroup(product, lines, factors, times)
        factor_group.next_to(words, DOWN, LARGE_BUFF, aligned_edge=RIGHT)

        self.play(FadeIn(product))
        self.play(
            LaggedStartMap(ShowCreation, lines, lag_ratio=0.25),
            LaggedStart(
                (TransformFromCopy(product, factor)
                for factor in factors),
                lag_ratio=0.25
            ),
            Write(times, time_span=(0.5, 1.5)),
        )
        self.wait()
