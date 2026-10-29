# ==============================================================================
# Scene:      MoreLinks
# Source:     videos/_2020/ctracing.py (lines 491-506)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreLinks.py MoreLinks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoreLinks(Scene):
    def construct(self):
        words = OldTexText("See more links\\\\in the description.")
        words.scale(2)
        words.to_edge(UP, buff=2)
        arrows = VGroup(*[
            Vector(1.5 * DOWN, stroke_width=10)
            for x in range(4)
        ])
        arrows.arrange(RIGHT, buff=0.75)
        arrows.next_to(words, DOWN, buff=0.5)
        for arrow, color in zip(arrows, [BLUE_D, BLUE_C, BLUE_E, GREY_BROWN]):
            arrow.set_color(color)
        self.play(Write(words))
        self.play(LaggedStartMap(ShowCreation, arrows))
        self.wait()
