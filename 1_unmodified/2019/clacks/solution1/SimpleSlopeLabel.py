# ==============================================================================
# Scene:      SimpleSlopeLabel
# Source:     videos/_2019/clacks/solution1.py (lines 1938-1951)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleSlopeLabel.py SimpleSlopeLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleSlopeLabel(Scene):
    def construct(self):
        label = OldTex(
            "\\text{Slope}", "=",
            "-\\frac{\\sqrt{m_1}}{\\sqrt{m_2}}"
        )
        vector = Vector(DOWN + 2 * LEFT, color=WHITE)
        vector.move_to(label[0].get_bottom(), UR)
        vector.shift(SMALL_BUFF * DOWN)
        self.play(
            Write(label),
            GrowArrow(vector),
        )
        self.wait()
