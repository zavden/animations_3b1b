# ==============================================================================
# Scene:      ArrowBetweenScreens
# Source:     videos/_2025/laplace/prequel_equations.py (lines 183-197)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrowBetweenScreens.py ArrowBetweenScreens -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ArrowBetweenScreens(InteractiveScene):
    def construct(self):
        # Test
        screens = ScreenRectangle().replicate(2)
        screens.arrange(RIGHT, buff=MED_LARGE_BUFF)
        screens.set_width(FRAME_WIDTH - 2)
        screens.move_to(DOWN)
        arrow = Arrow(screens[0].get_top(), screens[1].get_top(), path_arc=-120 * DEG, thickness=6, buff=0.25)
        line = Line(screens[0].get_top(), screens[1].get_top(), path_arc=-120 * DEG, stroke_width=8, buff=0.25)
        VGroup(arrow, line).set_color(TEAL)
        self.play(
            ShowCreation(line),
            FadeIn(arrow, time_span=(0.75, 1))
        )
        self.wait()
