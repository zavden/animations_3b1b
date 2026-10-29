# ==============================================================================
# Scene:      SwirlDiameterD
# Source:     videos/_2018/turbulence.py (lines 1390-1420)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SwirlDiameterD.py SwirlDiameterD -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SwirlDiameterD(Scene):
    def construct(self):
        kwargs = {
            "path_arc": PI,
            "buff": SMALL_BUFF,
            "color": WHITE
        }
        swirl = VGroup(
            Arrow(RIGHT, LEFT, **kwargs),
            Arrow(LEFT, RIGHT, **kwargs),
        )
        swirl.set_stroke(width=5)
        f = 1.5
        swirl.scale(f)

        h_line = DashedLine(
            f * LEFT, f * RIGHT,
            color=YELLOW,
        )
        D_label = OldTex("D")
        D_label.scale(2)
        D_label.next_to(h_line, UP, SMALL_BUFF)
        D_label.match_color(h_line)
        # diam = VGroup(h_line, D_label)

        self.play(*map(ShowCreation, swirl))
        self.play(
            GrowFromCenter(h_line),
            FadeIn(D_label, UP),
        )
        self.wait()
