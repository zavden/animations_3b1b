# ==============================================================================
# Scene:      OtherInstanceOfInverseSquareLaw
# Source:     videos/_2018/basel/basel2.py (lines 1884-1916)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OtherInstanceOfInverseSquareLaw.py OtherInstanceOfInverseSquareLaw -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class OtherInstanceOfInverseSquareLaw(Scene):
    def construct(self):
        title = OldTexText("Where the inverse square law shows up")
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        h_line.next_to(title, DOWN)
        self.add(title, h_line)

        items = VGroup(*[
            OldTexText("- %s"%s).scale(1)
            for s in [
                "Heat", "Sound", "Radio waves", "Electric fields",
            ]
        ])
        items.arrange(DOWN, buff = MED_LARGE_BUFF, aligned_edge = LEFT)
        items.next_to(h_line, DOWN, LARGE_BUFF)
        items.to_edge(LEFT)

        dot = Dot()
        dot.move_to(4*RIGHT)
        self.add(dot)
        def get_broadcast():
            return Broadcast(dot, big_radius = 5, run_time = 5)

        self.play(
            LaggedStartMap(FadeIn, items, run_time = 4, lag_ratio = 0.7),
            Succession(*[
                get_broadcast()
                for x in range(2)
            ])
        )
        self.play(get_broadcast())
        self.wait()
