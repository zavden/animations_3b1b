# ==============================================================================
# Scene:      MeasureTheoryLeadsTo
# Source:     videos/_2020/beta/beta2.py (lines 1917-1930)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MeasureTheoryLeadsTo.py MeasureTheoryLeadsTo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MeasureTheoryLeadsTo(Scene):
    def construct(self):
        words = OldTexText("Measure Theory")
        words.set_color(RED)
        arrow = Vector(DOWN)
        arrow.next_to(words, DOWN, buff=SMALL_BUFF)
        arrow.set_stroke(width=7)
        arrow.rotate(45 * DEGREES, about_point=arrow.get_start())
        self.play(
            FadeIn(words, DOWN),
            GrowArrow(arrow),
            UpdateFromAlphaFunc(arrow, lambda m, a: m.set_opacity(a)),
        )
        self.wait()
