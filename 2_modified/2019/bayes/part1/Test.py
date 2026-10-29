# ==============================================================================
# Scene:      Test
# Source:     videos/_2019/bayes/part1.py (lines 431-435)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Test.py Test -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class FarmerIcon(SVGMobject):
    CONFIG = {
        "file_name": "farming",
        "stroke_width": 0,
        "fill_color": GREEN_E,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "height": 1.5,
    }


class Test(Scene):
    def construct(self):
        icon = FarmerIcon()
        icon.scale(2)
        self.add(icon)
