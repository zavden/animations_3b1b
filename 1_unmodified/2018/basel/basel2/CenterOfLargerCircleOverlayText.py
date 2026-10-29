# ==============================================================================
# Scene:      CenterOfLargerCircleOverlayText
# Source:     videos/_2018/basel/basel2.py (lines 3759-3767)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CenterOfLargerCircleOverlayText.py CenterOfLargerCircleOverlayText -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class CenterOfLargerCircleOverlayText(Scene):
    def construct(self):
        words = OldTexText("Center of \\\\ larger circle")
        arrow = Vector(DOWN+LEFT, color = WHITE)
        arrow.shift(words.get_bottom() + SMALL_BUFF*DOWN - arrow.get_start())
        group = VGroup(words, arrow)
        group.set_height(FRAME_HEIGHT - 1)
        group.to_edge(UP)
        self.add(group)
