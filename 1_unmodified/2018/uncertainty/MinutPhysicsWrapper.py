# ==============================================================================
# Scene:      MinutPhysicsWrapper
# Source:     videos/_2018/uncertainty.py (lines 3674-3689)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MinutPhysicsWrapper.py MinutPhysicsWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class MinutPhysicsWrapper(Scene):
    def construct(self):
        logo = ImageMobject("minute_physics_logo", invert = True)
        logo.to_corner(UP+LEFT)
        self.add(logo)

        title = OldTexText("Minute Physics on special relativity")
        title.to_edge(UP).shift(MED_LARGE_BUFF*RIGHT)

        screen_rect = ScreenRectangle()
        screen_rect.set_width(title.get_width() + LARGE_BUFF)
        screen_rect.next_to(title, DOWN)

        self.play(ShowCreation(screen_rect))
        self.play(Write(title))
        self.wait(2)
