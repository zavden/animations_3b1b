# ==============================================================================
# Scene:      Thumbnail4
# Source:     videos/_2020/med_test.py (lines 273-296)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail4.py Thumbnail4 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail4(Scene):
    def construct(self):
        top_words = Text("False Positive Rate")
        top_words.set_width(FRAME_WIDTH - 1)
        top_words.to_edge(UP)
        self.add(top_words)

        # is_not = Text("is NOT")
        is_not = OldTex("\\ne")
        is_not.set_color(RED)
        is_not.set_height(2.5)
        is_not.set_stroke(RED, 8)
        self.add(is_not)

        prob = Text(
            "P(Healthy | Positive)",
            t2c={
                "Healthy": YELLOW,
                "Positive": GREEN,
            }
        )
        prob.set_width(FRAME_WIDTH - 1)
        prob.to_edge(DOWN)
        self.add(prob)
