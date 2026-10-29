# ==============================================================================
# Scene:      ArrowScene
# Source:     videos/_2018/turbulence.py (lines 1779-1783)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrowScene.py ArrowScene -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ArrowScene(Scene):
    def construct(self):
        arrow = Arrow(LEFT, RIGHT, color=WHITE)
        arrow.add_to_back(arrow.copy().set_stroke(BLACK, 5))
        self.add(arrow)
