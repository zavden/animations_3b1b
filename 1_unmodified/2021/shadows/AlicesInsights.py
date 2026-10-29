# ==============================================================================
# Scene:      AlicesInsights
# Source:     videos/_2021/shadows.py (lines 4006-4044)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AlicesInsights.py AlicesInsights -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AlicesInsights(Scene):
    def construct(self):
        title = OldTexText("Alice's insights", font_size=72)
        title.to_edge(UP)
        title.set_backstroke()
        underline = Underline(title, buff=-0.05)
        underline.scale(1.5)
        underline.insert_n_curves(50)
        underline.set_stroke(WHITE, width=[0, *4 * [3], 0], opacity=1)
        self.add(underline, title)

        kw = dict(
            t2c={
                "double cover": YELLOW,
                "mean": RED,
                "means": RED,
                "sum": BLUE,
                "Sum": BLUE,
                "Average": RED,
            }
        )
        insights = VGroup(
            Text("1. The face shadows double cover the cube shadow", **kw),
            # Text("2. The mean of the sum is the sum of the means", **kw),
            Text("2. Average(Sum(Face shadows)) = Sum(Average(Face shadow))", **kw),
            Text("3. Use a sphere to deduce the unknown constant", **kw),
        )
        insights.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        insights.next_to(underline, DOWN, LARGE_BUFF)
        insights.to_edge(LEFT)

        self.play(LaggedStart(*(
            FadeIn(insight[:2], 0.25 * DOWN)
            for insight in insights
        )))
        self.wait()
        for insight in insights:
            self.play(FadeIn(insight[2:], lag_ratio=0.1))
            self.wait()
