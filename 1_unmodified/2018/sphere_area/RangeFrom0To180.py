# ==============================================================================
# Scene:      RangeFrom0To180
# Source:     videos/_2018/sphere_area.py (lines 3292-3303)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RangeFrom0To180.py RangeFrom0To180 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RangeFrom0To180(Scene):
    def construct(self):
        angle = Integer(0, unit="^\\circ")
        angle.scale(2)

        self.add(angle)
        self.wait()
        self.play(ChangeDecimalToValue(
            angle, 180,
            run_time=2,
        ))
        self.wait()
