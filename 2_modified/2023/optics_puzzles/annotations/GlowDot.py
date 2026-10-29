# ==============================================================================
# Scene:      GlowDot
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1285-1296)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GlowDot.py GlowDot -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The scene is called GlowDot and shadows manimlib's GlowDot class (GlowDot(radius=3) called the scene: a bug in the original); the class is imported as _GlowDotMobject
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

# CHANGE: the scene is called GlowDot and shadows manimlib's GlowDot class (in the original GlowDot(radius=3, ...) called the scene and failed); the class is imported under another name
from manimlib.mobject.types.dot_cloud import GlowDot as _GlowDotMobject


class GlowDot(InteractiveScene):
    def construct(self):
        self.add(_GlowDotMobject(radius=3, color=WHITE))

        mid_point = 0.85 * LEFT
        mask = VMobject().set_points_as_corners([
            UR, mid_point, DR, DL, UL,
        ])
        mask.set_fill(BLACK, 1)
        mask.set_stroke(width=0)
        mask.set_height(20, about_point=mid_point)
        self.add(mask)
