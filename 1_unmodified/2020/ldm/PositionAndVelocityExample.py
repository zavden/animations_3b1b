# ==============================================================================
# Scene:      PositionAndVelocityExample
# Source:     videos/_2020/ldm.py (lines 758-764)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PositionAndVelocityExample.py PositionAndVelocityExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PositionAndVelocityExample(Scene):
    def construct(self):
        plane = NumberPlane()

        self.add(plane)

        self.embed()
