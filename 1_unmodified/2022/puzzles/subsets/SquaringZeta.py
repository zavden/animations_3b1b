# ==============================================================================
# Scene:      SquaringZeta
# Source:     videos/_2022/puzzles/subsets.py (lines 4834-4861)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SquaringZeta.py SquaringZeta -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SquaringZeta(InteractiveScene):
    def construct(self):
        # Magnitude
        kw = dict(tex_to_color_map={"\\zeta": YELLOW})
        mag = Tex("|\\zeta^2| = |\\zeta|^2 = 1^2 = 1", **kw)
        mag.move_to(2 * UR)

        self.play(FadeIn(mag[:4]))
        self.play(TransformMatchingShapes(mag[:4].copy(), mag[4:9]))
        self.play(TransformMatchingShapes(mag[4:9].copy(), mag[9:12]))
        self.play(TransformMatchingShapes(mag[9:12].copy(), mag[12:]))
        self.wait()

        # Explicit
        exp = Tex(
            "\\zeta^2 ="
            "\\big(e^{2\\pi i / 5}\\big)^2 ="
            "e^{4\\pi i / 5}",
            **kw
        )
        exp.next_to(mag, DOWN, LARGE_BUFF, aligned_edge=LEFT)
        rect = SurroundingRectangle(exp[-5:], buff=0.05)
        rect.set_stroke(YELLOW, 2)

        self.play(FadeIn(exp, lag_ratio=0.1))
        self.play(ShowCreation(rect))
        self.wait()
        self.play(FadeOut(rect))
