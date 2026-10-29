# ==============================================================================
# Scene:      GeneralWrapper
# Source:     videos/_2018/fc1.py (lines 205-216)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneralWrapper.py GeneralWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneralWrapper(Scene):
    CONFIG = {
        "title_text": ""
    }

    def construct(self):
        title = OldTexText(self.title_text)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6.5)
        rect.next_to(title, DOWN)
        self.play(Write(title), ShowCreation(rect))
        self.wait()
