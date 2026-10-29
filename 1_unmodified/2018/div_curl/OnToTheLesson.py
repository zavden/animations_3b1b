# ==============================================================================
# Scene:      OnToTheLesson
# Source:     videos/_2018/div_curl.py (lines 1090-1096)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OnToTheLesson.py OnToTheLesson -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OnToTheLesson(Scene):
    def construct(self):
        words = OldTexText("On to the lesson!")
        words.scale(1.5)
        self.add(words)
        self.play(FadeInFromDown(words))
        self.wait()
