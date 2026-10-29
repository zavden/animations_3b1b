# ==============================================================================
# Scene:      SimpleExpToPole
# Source:     videos/_2025/laplace/main_equations.py (lines 1749-1774)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleExpToPole.py SimpleExpToPole -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleExpToPole(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"{t}": BLUE, "{s}": YELLOW}
        kw = dict(t2c=t2c, font_size=72)
        lhs, arrow, rhs = group = VGroup(
            Tex(R"e^{a{t}}", **kw),
            Vector(1.5 * RIGHT, thickness=5),
            Tex(R"{1 \over {s} - a}", **kw)
        )
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.to_edge(UP, MED_LARGE_BUFF)
        fancy_L = Tex(R"\mathcal{L}")
        fancy_L.next_to(arrow, UP, SMALL_BUFF)

        self.play(FadeIn(lhs))
        self.play(
            GrowArrow(arrow),
            Write(fancy_L),
            run_time=1,
        )
        self.play(
            Write(rhs[:-1]),
            TransformFromCopy(lhs["a"], rhs["a"])
        )
        self.wait()
