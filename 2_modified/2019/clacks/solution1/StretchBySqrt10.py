# ==============================================================================
# Scene:      StretchBySqrt10
# Source:     videos/_2019/clacks/solution1.py (lines 1143-1155)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl StretchBySqrt10.py StretchBySqrt10 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Apply the small adjustment to GL's whole tip instead of indexing nonexistent subparts.
# ==============================================================================

from manim_imports_ext import *

class StretchBySqrt10(Scene):
    def construct(self):
        arrow = DoubleArrow(2 * LEFT, 2 * RIGHT)
        # CHANGE: GL's arrow tip is a single shape rather than a two-part group.
        arrow.tip.shift(0.05 * LEFT)
        value = OldTex("\\sqrt{10}")
        value.next_to(arrow, UP)
        arrow.save_state()
        arrow.stretch(0, 0)
        self.play(
            Restore(arrow),
            Write(value, run_time=1),
        )
        self.wait()
