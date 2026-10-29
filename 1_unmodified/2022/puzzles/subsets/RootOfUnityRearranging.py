# ==============================================================================
# Scene:      RootOfUnityRearranging
# Source:     videos/_2022/puzzles/subsets.py (lines 5165-5196)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RootOfUnityRearranging.py RootOfUnityRearranging -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RootOfUnityRearranging(InteractiveScene):
    def construct(self):
        kw = dict(tex_to_color_map={"\\zeta": YELLOW})
        expressions = VGroup(
            Tex("z^5 = 1", **kw),
            Tex("z^5 - 1 = 0", **kw),
            Tex("z^5 - 1 = (z - \\zeta^0)(z - \\zeta^1)(z - \\zeta^2)(z - \\zeta^3)(z - \\zeta^4)", **kw),
        )
        expressions[:2].scale(1.5, about_edge=UP)
        subtexts = VGroup(
            Tex("\\text{Solutions: } \\zeta^0,\\, \\zeta^1,\\, \\zeta^2,\\, \\zeta^3,\\, \\zeta^4", **kw),
            Tex("\\text{Roots: } \\zeta^0,\\, \\zeta^1,\\, \\zeta^2,\\, \\zeta^3,\\, \\zeta^4", **kw),
        )
        subtexts.next_to(expressions, DOWN, LARGE_BUFF)

        self.play(FadeIn(expressions[0]))
        self.play(Write(subtexts[0]))
        self.wait()
        self.play(
            TransformMatchingShapes(*expressions[:2]),
            FadeTransform(*subtexts[:2]),
        )
        self.wait()
        self.play(
            expressions[1].animate.move_to(expressions[2], LEFT)
        )
        self.play(
            FadeOut(expressions[1][-1]),
            FadeTransform(expressions[1][:5], expressions[2][:5]),
            TransformMatchingShapes(subtexts[1], expressions[2][5:]),
        )
        self.wait()
