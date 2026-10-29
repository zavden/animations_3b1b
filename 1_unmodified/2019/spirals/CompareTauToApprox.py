# ==============================================================================
# Scene:      CompareTauToApprox
# Source:     videos/_2019/spirals.py (lines 3192-3211)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareTauToApprox.py CompareTauToApprox -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareTauToApprox(Scene):
    def construct(self):
        eqs = VGroup(
            OldTex("2\\pi", "=", "{:.10}\\dots".format(TAU)),
            OldTex("\\frac{710}{113}", "=", "{:.10}\\dots".format(710 / 113)),
        )
        eqs.arrange(DOWN, buff=LARGE_BUFF)
        eqs[1].shift((eqs[0][2].get_left()[0] - eqs[1][2].get_left()[0]) * RIGHT)

        eqs.generate_target()
        for eq in eqs.target:
            eq[2][:8].set_color(RED)
            eq.set_stroke(BLACK, 8, background=True)

        self.play(LaggedStart(
            FadeIn(eqs[0], DOWN),
            FadeIn(eqs[1], UP),
        ))
        self.play(MoveToTarget(eqs))
        self.wait()
