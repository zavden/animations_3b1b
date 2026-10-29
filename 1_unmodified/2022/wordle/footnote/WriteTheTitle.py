# ==============================================================================
# Scene:      WriteTheTitle
# Source:     videos/_2022/wordle/footnote.py (lines 49-54)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteTheTitle.py WriteTheTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteTheTitle(Scene):
    def construct(self):
        title = Text("Solving Wordle using\ninformation theory", font_size=60)
        title.get_part_by_text('information theory').set_color(BLUE)
        self.play(Write(title))
        self.wait()
