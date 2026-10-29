# ==============================================================================
# Scene:      AtomsOfCalculus
# Source:     videos/_2025/laplace/prequel_equations.py (lines 1624-1642)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AtomsOfCalculus.py AtomsOfCalculus -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AtomsOfCalculus(InteractiveScene):
    def construct(self):
        # Test
        expr = Tex(R"e^{s_n t}", font_size=72)
        expr.to_edge(RIGHT, buff=LARGE_BUFF)
        rect = SurroundingRectangle(expr, buff=SMALL_BUFF)
        rect.set_stroke(YELLOW, 2)
        words = Text("Atoms of\nCalculus", font_size=60)
        words.set_x(FRAME_WIDTH / 5)
        words.set_y(3)
        arrow = Arrow(words.get_right(), rect.get_top(), path_arc=-90 * DEG, thickness=4)
        arrow.set_fill(YELLOW)

        self.play(LaggedStart(
            Write(words),
            Write(arrow),
            ShowCreation(rect)
        ))
        self.wait()
