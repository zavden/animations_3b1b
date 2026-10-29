# ==============================================================================
# Scene:      SpecialThanks
# Source:     videos/_2018/pi_day.py (lines 970-989)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SpecialThanks.py SpecialThanks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SpecialThanks(Scene):
    def construct(self):
        title = OldTexText("Special thanks to:")
        title.to_edge(UP, LARGE_BUFF)
        title.scale(1.5)
        title.set_color(BLUE)
        h_line = Line(LEFT, RIGHT).scale(4)
        h_line.next_to(title, DOWN)
        h_line.set_stroke(WHITE, 1)

        people = VGroup(*list(map(TexText, [
            "Ben Hambrecht",
            "University Library Basel",
            "Martin Mattmüller",
            "Library of the Institut de France",
        ])))
        people.arrange(DOWN, aligned_edge = LEFT, buff = MED_LARGE_BUFF)
        people.next_to(h_line, DOWN)

        self.add(title, h_line, people)
