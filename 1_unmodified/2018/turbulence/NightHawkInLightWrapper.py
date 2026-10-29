# ==============================================================================
# Scene:      NightHawkInLightWrapper
# Source:     videos/_2018/turbulence.py (lines 548-557)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NightHawkInLightWrapper.py NightHawkInLightWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NightHawkInLightWrapper(Scene):
    def construct(self):
        title = OldTexText("NightHawkInLight")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)
        self.add(title)
        self.play(ShowCreation(rect))
        self.wait()
