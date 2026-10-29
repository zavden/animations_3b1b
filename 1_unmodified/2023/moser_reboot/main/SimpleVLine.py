# ==============================================================================
# Scene:      SimpleVLine
# Source:     videos/_2023/moser_reboot/main.py (lines 689-693)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleVLine.py SimpleVLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleVLine(InteractiveScene):
    def construct(self):
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.set_stroke(GREY_C, 2)
        self.add(v_line)
