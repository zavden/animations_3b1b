# ==============================================================================
# Scene:      PhaseSpaceTitle
# Source:     videos/_2019/clacks/solution1.py (lines 168-177)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PhaseSpaceTitle.py PhaseSpaceTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PhaseSpaceTitle(Scene):
    def construct(self):
        title = OldTexText("Phase space")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)
        self.add(rect)
        self.play(Write(title, run_time=1))
        self.wait()
