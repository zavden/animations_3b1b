# ==============================================================================
# Scene:      MathologerVideoWrapper
# Source:     videos/_2018/basel/basel2.py (lines 2330-2351)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MathologerVideoWrapper.py MathologerVideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class MathologerVideoWrapper(Scene):
    def construct(self):
        title = OldTexText("""
            Mathologer's excellent video on \\\\
            the many Pythagorean theorem cousins
        """)
        # title.scale(0.7)
        title.to_edge(UP)
        logo = ImageMobject("mathologer_logo")
        logo.set_height(1)
        logo.to_corner(UP+LEFT)
        logo.shift(FRAME_WIDTH*RIGHT)
        screen = ScreenRectangle(height = 5.5)
        screen.next_to(title, DOWN)

        self.play(
            logo.shift, FRAME_WIDTH*LEFT,
            LaggedStartMap(FadeIn, title),
            run_time = 2
        )
        self.play(ShowCreation(screen))
        self.wait(5)
