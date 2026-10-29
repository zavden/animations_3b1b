# ==============================================================================
# Scene:      ThreeBodyTitle
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 473-478)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeBodyTitle.py ThreeBodyTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeBodyTitle(Scene):
    def construct(self):
        title = OldTexText("Three body problem")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)
