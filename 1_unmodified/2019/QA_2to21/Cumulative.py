# ==============================================================================
# Scene:      Cumulative
# Source:     videos/_2019/QA_2to21.py (lines 161-219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Cumulative.py Cumulative -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Cumulative(Scene):
    def construct(self):
        colors = list(Color(BLUE_B).range_to(BLUE_D, 20))
        rects = VGroup(*[
            Rectangle(
                height=0.3, width=4,
                fill_color=random.choice(colors),
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1,
            )
            for i, color in zip(range(20), it.cycle(colors))
        ])
        rects.arrange(UP, buff=0)

        check = OldTex("\\checkmark").set_color(GREEN)
        cross = OldTex("\\times").set_color(RED)
        checks, crosses = [
            VGroup(*[
                mob.copy().next_to(rect, RIGHT, SMALL_BUFF)
                for rect in rects
            ])
            for mob in [check, cross]
        ]

        rects.set_fill(opacity=0)
        self.add(rects)

        for i in range(7):
            self.play(
                rects[i].set_fill, None, 1.0,
                Write(checks[i]),
                run_time=0.5,
            )
        self.play(FadeOut(rects[7], 2 * LEFT))
        self.play(
            LaggedStartMap(Write, crosses[8:]),
            LaggedStartMap(
                ApplyMethod, rects[8:],
                lambda m: (m.set_fill, None, 0.2),
            )
        )
        self.wait()
        rects[7].set_opacity(1)
        self.play(
            FadeIn(rects[7], 2 * LEFT),
            FadeIn(checks[7], 2 * LEFT),
        )
        self.play(
            LaggedStartMap(
                ApplyMethod, rects[8:],
                lambda m: (m.set_fill, None, 1.0),
            ),
            LaggedStart(*[
                ReplacementTransform(cross, check)
                for cross, check in zip(crosses[8:], checks[8:])
            ])
        )
        self.wait()
