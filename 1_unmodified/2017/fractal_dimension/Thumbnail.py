# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2017/fractal_dimension.py (lines 2918-2931)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(Scene):
    def construct(self):
        title = OldTexText("1.5-dimensional")
        title.scale(2)
        title.to_edge(UP)


        koch_curve = QuadraticKoch(order = 6, monochromatic = True)
        koch_curve.set_stroke(width = 0)
        koch_curve.set_fill(BLUE)
        koch_curve.set_height(1.5*FRAME_Y_RADIUS)
        koch_curve.to_edge(DOWN, buff = SMALL_BUFF)

        self.add(koch_curve, title)
