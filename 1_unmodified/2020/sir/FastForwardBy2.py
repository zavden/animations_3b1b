# ==============================================================================
# Scene:      FastForwardBy2
# Source:     videos/_2020/sir.py (lines 2255-2288)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FastForwardBy2.py FastForwardBy2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FastForwardBy2(Scene):
    CONFIG = {
        "n": 2,
    }

    def construct(self):
        n = self.n
        triangles = VGroup(*[
            ArrowTip(start_angle=0)
            for x in range(n)
        ])
        triangles.arrange(RIGHT, buff=0.01)

        label = VGroup(OldTex("\\times"), Integer(n))
        label.set_height(0.4)
        label.arrange(RIGHT, buff=SMALL_BUFF)
        label.next_to(triangles, RIGHT, buff=SMALL_BUFF)

        for mob in triangles, label:
            mob.set_color(GREY_A)
            mob.set_stroke(BLACK, 4, background=True)

        self.play(
            LaggedStartMap(
                FadeInFrom, triangles,
                lambda m: (m, 0.4 * LEFT),
            ),
            FadeIn(label, 0.2 * LEFT),
            run_time=1,
        )
        self.play(
            FadeOut(label),
            FadeOut(triangles),
        )
