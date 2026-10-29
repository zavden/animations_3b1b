# ==============================================================================
# Scene:      VLineOverZero
# Source:     videos/_2025/laplace/prequel_equations.py (lines 670-683)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VLineOverZero.py VLineOverZero -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VLineOverZero(InteractiveScene):
    def construct(self):
        # Test
        rect = Square(0.25)
        rect.move_to(2.5 * DOWN)
        v_line = Line(rect.get_top(), 4 * UP, buff=0.1)
        v_line.set_stroke(YELLOW, 2)
        rect.match_style(v_line)

        self.play(
            ShowCreationThenFadeOut(rect),
            ShowCreationThenFadeOut(v_line),
        )
        self.wait()
