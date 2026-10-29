# ==============================================================================
# Scene:      InterpolationFail
# Source:     videos/_2018/quat3d.py (lines 789-796)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InterpolationFail.py InterpolationFail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InterpolationFail(Scene):
    def construct(self):
        words = OldTexText(
            "Sometimes interpolating 3d\\\\"
            "orientations is tricky..."
        )
        words.to_edge(UP)
        self.add(words)
