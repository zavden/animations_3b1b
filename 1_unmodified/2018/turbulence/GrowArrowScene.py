# ==============================================================================
# Scene:      GrowArrowScene
# Source:     videos/_2018/turbulence.py (lines 1354-1358)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GrowArrowScene.py GrowArrowScene -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GrowArrowScene(Scene):
    def construct(self):
        arrow = Arrow(UP, DOWN, color=WHITE)
        self.play(GrowArrow(arrow))
        self.wait()
