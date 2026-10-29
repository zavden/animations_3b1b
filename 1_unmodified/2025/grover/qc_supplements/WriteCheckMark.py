# ==============================================================================
# Scene:      WriteCheckMark
# Source:     videos/_2025/grover/qc_supplements.py (lines 304-314)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteCheckMark.py WriteCheckMark -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteCheckMark(InteractiveScene):
    def construct(self):
        # Test
        check = Checkmark()
        check.set_color(GREEN)
        check.set_height(0.75)
        self.play(
            Write(check),
            Flash(check.get_left() + 1.0 * LEFT, flash_radius=0.8, line_length=0.2, color=GREEN)
        )
        self.wait()
