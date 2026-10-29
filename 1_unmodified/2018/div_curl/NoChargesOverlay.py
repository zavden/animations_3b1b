# ==============================================================================
# Scene:      NoChargesOverlay
# Source:     videos/_2018/div_curl.py (lines 4120-4132)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NoChargesOverlay.py NoChargesOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NoChargesOverlay(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle()
        rect.set_fill(BLUE_D, 0.75)
        circle = Circle(radius=1.5, num_anchors=5000)
        circle.rotate(135 * DEGREES)
        rect.add_subpath(circle.get_points())

        words = OldTexText("No charges outside wire")
        words.scale(1.5)
        words.to_edge(UP)

        self.add(rect, words)
