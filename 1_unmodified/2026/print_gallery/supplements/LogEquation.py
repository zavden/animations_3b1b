# ==============================================================================
# Scene:      LogEquation
# Source:     videos/_2026/print_gallery/supplements.py (lines 376-385)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LogEquation.py LogEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LogEquation(InteractiveScene):
    def construct(self):
        group = VGroup(
            Tex(R"=").rotate(90 * DEG),
            Tex(R"\ln(w \cdot 16)", t2c={"w": RED})
        )
        group.arrange(DOWN)
        group.set_backstroke(BLACK, 3)
        self.play(Write(group))
        self.wait()
