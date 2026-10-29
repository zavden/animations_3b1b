# ==============================================================================
# Scene:      SlowMotionLabel
# Source:     videos/_2019/clacks/question.py (lines 794-799)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SlowMotionLabel.py SlowMotionLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SlowMotionLabel(Scene):
    def construct(self):
        words = OldTexText("Slow motion replay")
        words.scale(2).to_edge(UP)
        self.play(Write(words))
        self.wait()
