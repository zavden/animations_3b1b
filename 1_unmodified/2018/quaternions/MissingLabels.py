# ==============================================================================
# Scene:      MissingLabels
# Source:     videos/_2018/quaternions.py (lines 5114-5123)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MissingLabels.py MissingLabels -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MissingLabels(Scene):
    def construct(self):
        labels = VGroup(
            OldTex("i").move_to(UR),
            OldTex("1").move_to(0.3 * DOWN),
            OldTex("-i").move_to(DOWN + 1.2 * LEFT),
            OldTex("-j").move_to(1.7 * RIGHT + 0.8 * DOWN),
        )
        labels.set_background_stroke(width=0)
        self.add(labels)
