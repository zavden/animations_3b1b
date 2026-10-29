# ==============================================================================
# Scene:      GeneratingfunctionologyTitle
# Source:     videos/_2022/puzzles/subsets.py (lines 5418-5427)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneratingfunctionologyTitle.py GeneratingfunctionologyTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneratingfunctionologyTitle(InteractiveScene):
    def construct(self):
        title = Text("Generatingfunctionology", font_size=60)
        author = Text("by Herbert Wilf")
        author.next_to(title, DOWN, MED_LARGE_BUFF, LEFT)
        author.set_color(GREY_B)

        self.play(Write(title))
        self.play(FadeIn(author, LEFT))
        self.wait()
