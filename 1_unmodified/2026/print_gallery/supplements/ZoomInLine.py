# ==============================================================================
# Scene:      ZoomInLine
# Source:     videos/_2026/print_gallery/supplements.py (lines 716-730)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ZoomInLine.py ZoomInLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ZoomInLine(InteractiveScene):
    def construct(self):
        # Test
        small_point = SMALL_BUFF * DL
        line = Line(16 * small_point, small_point)
        line.set_stroke(RED, width=(8, 3))
        dot = Dot(line.get_start())
        dot.set_color(RED)
        self.play(FadeIn(dot))
        self.play(
            ShowCreation(line),
            TransformFromCopy(dot, dot.copy().scale(0.25).move_to(line.get_end())),
            run_time=3
        )
        self.wait()
