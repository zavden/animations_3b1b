# ==============================================================================
# Scene:      VideoOnPhysicsGirlWrapper
# Source:     videos/_2018/turbulence.py (lines 520-530)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VideoOnPhysicsGirlWrapper.py VideoOnPhysicsGirlWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VideoOnPhysicsGirlWrapper(Scene):
    def construct(self):
        rect = ScreenRectangle(height=6)
        title = OldTexText("Video on Physics Girl")
        title.scale(1.5)
        title.to_edge(UP)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait()
