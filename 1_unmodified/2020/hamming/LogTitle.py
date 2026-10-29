# ==============================================================================
# Scene:      LogTitle
# Source:     videos/_2020/hamming.py (lines 5930-5940)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LogTitle.py LogTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LogTitle(Scene):
    def construct(self):
        title = OldTexText("$\\text{log}_2(256) = 8$ parity checks")
        title.set_height(0.7)
        title.to_edge(UP)
        underline = Underline(title[0][:4])
        underline.set_color(YELLOW)
        self.add(title)
        self.wait()
        self.play(ShowCreationThenFadeOut(underline))
        self.wait()
