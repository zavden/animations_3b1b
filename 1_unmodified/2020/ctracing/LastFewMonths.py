# ==============================================================================
# Scene:      LastFewMonths
# Source:     videos/_2020/ctracing.py (lines 5-20)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LastFewMonths.py LastFewMonths -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LastFewMonths(Scene):
    def construct(self):
        words = OldTexText("Last ", "few\\\\", "months:")
        words.set_height(4)
        underlines = VGroup()
        for word in words:
            underline = Line(LEFT, RIGHT)
            underline.match_width(word)
            underline.next_to(word, DOWN, SMALL_BUFF)
            underlines.add(underline)
        underlines[0].stretch(1.4, 0, about_edge=LEFT)
        underlines.set_color(BLUE)

        # self.play(ShowCreation(underlines))
        self.play(ShowIncreasingSubsets(words, run_time=0.75, rate_func=linear))
        self.wait()
